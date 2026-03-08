# -*- coding: utf-8 -*-
import logging
from odoo import api, SUPERUSER_ID

_logger = logging.getLogger(__name__)

# Field mapping: education.parent field -> res.partner field
FIELD_MAP = {
    'name': 'name',
    'phone': 'phone',
    'mobile': 'mobile',
    'email': 'email',
    'job': 'function',
    'workplace': 'workplace',
    'relation': 'guardian_relation',
    'marital_status': 'parent_social_status',
    'address': 'street',
    'id_number': 'id_number',
    'photo': 'image_1920',
    'notes': 'comment',
    'active': 'active',
    'job_number': 'job_number',
    'education_level': 'education_level',
    'mother_name': 'mother_name',
    'mother_phone': 'mother_phone',
    'mother_national_id': 'mother_national_id',
    'mother_education': 'mother_education',
}

# Marital status mapping (old values -> new values)
MARITAL_STATUS_MAP = {
    'married': 'married',
    'divorced': 'divorced',
    'widowed': 'widowed',
    'single': 'separated',  # closest match
}

# Education level mapping (old values -> new values)
EDUCATION_LEVEL_MAP = {
    'primary': 'primary',
    'secondary': 'secondary',
    'diploma': 'secondary',  # map to closest
    'bachelor': 'university',
    'master': 'postgraduate',
    'phd': 'postgraduate',
}


def migrate(cr, version):
    """Migrate education.parent records to res.partner with is_guardian=True."""
    env = api.Environment(cr, SUPERUSER_ID, {})
    _logger.info("Starting guardian migration from education.parent to res.partner")

    # Check if education_parent table exists
    cr.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_name = 'education_parent'
        )
    """)
    if not cr.fetchone()[0]:
        _logger.info("education_parent table does not exist, skipping migration")
        return

    # Fetch all education.parent records
    cr.execute("""
        SELECT id, name, phone, mobile, email, job, workplace,
               relation, marital_status, address, id_number,
               photo, notes, active, nationality, job_number,
               education_level, mother_name, mother_phone,
               mother_national_id, mother_education, city_id
        FROM education_parent
    """)
    parent_records = cr.fetchall()
    columns = [desc[0] for desc in cr.description]

    old_to_new = {}  # old parent ID -> new partner ID

    for row in parent_records:
        record = dict(zip(columns, row))
        old_id = record['id']

        # Map marital status
        social_status = MARITAL_STATUS_MAP.get(
            record.get('marital_status'), record.get('marital_status'))

        # Map education level
        edu_level = EDUCATION_LEVEL_MAP.get(
            record.get('education_level'), record.get('education_level'))
        mother_edu = EDUCATION_LEVEL_MAP.get(
            record.get('mother_education'), record.get('mother_education'))

        partner_vals = {
            'name': record['name'] or 'Unknown Guardian',
            'phone': record.get('phone'),
            'mobile': record.get('mobile'),
            'email': record.get('email'),
            'function': record.get('job'),
            'workplace': record.get('workplace'),
            'guardian_relation': record.get('relation'),
            'parent_social_status': social_status,
            'street': record.get('address'),
            'id_number': record.get('id_number'),
            'image_1920': record.get('photo'),
            'comment': record.get('notes'),
            'active': record.get('active', True),
            'is_guardian': True,
            'country_id': record.get('nationality'),
            'job_number': record.get('job_number'),
            'education_level': edu_level,
            'mother_name': record.get('mother_name'),
            'mother_phone': record.get('mother_phone'),
            'mother_national_id': record.get('mother_national_id'),
            'mother_education': mother_edu,
            'guardian_city_id': record.get('city_id'),
        }

        # Remove None values for cleaner insert
        partner_vals = {k: v for k, v in partner_vals.items() if v is not None}

        new_partner = env['res.partner'].create(partner_vals)
        old_to_new[old_id] = new_partner.id
        _logger.info(
            "Migrated education.parent %s -> res.partner %s (%s)",
            old_id, new_partner.id, record['name'])

    _logger.info("Migrated %d guardian records", len(old_to_new))

    # Update FK references in education_student (father_id, mother_id)
    for old_id, new_id in old_to_new.items():
        cr.execute("""
            UPDATE education_student
            SET father_id = %s
            WHERE father_id = %s
        """, (new_id, old_id))

        cr.execute("""
            UPDATE education_student
            SET mother_id = %s
            WHERE mother_id = %s
        """, (new_id, old_id))

    # Update FK in education_kids_area_booking (parent_id)
    cr.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_name = 'education_kids_area_booking'
        )
    """)
    if cr.fetchone()[0]:
        for old_id, new_id in old_to_new.items():
            cr.execute("""
                UPDATE education_kids_area_booking
                SET parent_id = %s
                WHERE parent_id = %s
            """, (new_id, old_id))

    # Update FK in education_student_transport (parent_id)
    # Note: parent_id is a related field, so we don't need to update it directly
    # It will be recomputed from student_id.father_id

    # Migrate mail.message records
    for old_id, new_id in old_to_new.items():
        cr.execute("""
            UPDATE mail_message
            SET model = 'res.partner', res_id = %s
            WHERE model = 'education.parent' AND res_id = %s
        """, (new_id, old_id))

    # Migrate mail.activity records
    cr.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.columns
            WHERE table_name = 'mail_activity' AND column_name = 'res_model'
        )
    """)
    if cr.fetchone()[0]:
        for old_id, new_id in old_to_new.items():
            cr.execute("""
                UPDATE mail_activity
                SET res_model = 'res.partner', res_id = %s
                WHERE res_model = 'education.parent' AND res_id = %s
            """, (new_id, old_id))

    _logger.info("Guardian migration completed successfully")
