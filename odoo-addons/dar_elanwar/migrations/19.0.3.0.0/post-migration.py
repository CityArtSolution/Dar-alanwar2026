# -*- coding: utf-8 -*-
import logging
from odoo import api, SUPERUSER_ID

_logger = logging.getLogger(__name__)

# Field mapping: education_parent column -> res.partner ORM field
FIELD_MAP = {
    'name': 'name',
    'phone': 'phone',
    'mobile': 'mobile',
    'email': 'email',
    'job': 'function',
    'workplace': 'workplace',
    'relation': 'guardian_relation',
    'address': 'street',
    'id_number': 'id_number',
    'notes': 'comment',
    'active': 'active',
    'job_number': 'job_number',
    'education_level': 'education_level',
    'mother_name': 'mother_name',
    'mother_phone': 'mother_phone',
    'mother_national_id': 'mother_national_id',
    'mother_education': 'mother_education',
    'nationality': 'country_id',
    'country_id': 'country_id',
    'city_id': 'guardian_city_id',
    'marital_status': 'parent_social_status',
}


def _table_exists(cr, table_name):
    cr.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_name = %s
        )
    """, (table_name,))
    return cr.fetchone()[0]


def _get_table_columns(cr, table_name):
    cr.execute("""
        SELECT column_name FROM information_schema.columns
        WHERE table_name = %s
    """, (table_name,))
    return {row[0] for row in cr.fetchall()}


def migrate(cr, version):
    """Migrate education.parent records to res.partner with is_guardian=True."""
    env = api.Environment(cr, SUPERUSER_ID, {})
    _logger.info("Starting guardian migration from education.parent to res.partner")

    if not _table_exists(cr, 'education_parent'):
        _logger.info("education_parent table does not exist, skipping migration")
        return

    # Dynamically detect available columns
    available_cols = _get_table_columns(cr, 'education_parent')
    _logger.info("education_parent columns: %s", available_cols)

    # Build SELECT with only existing columns
    select_cols = ['id']
    for col in FIELD_MAP:
        if col in available_cols:
            select_cols.append(col)

    cr.execute("SELECT %s FROM education_parent" % ', '.join(select_cols))
    parent_records = cr.fetchall()
    columns = [desc[0] for desc in cr.description]

    old_to_new = {}

    for row in parent_records:
        record = dict(zip(columns, row))
        old_id = record['id']

        partner_vals = {
            'is_guardian': True,
            'name': record.get('name') or 'Unknown Guardian',
        }

        for src_col, dst_field in FIELD_MAP.items():
            if src_col in record and record[src_col] is not None:
                partner_vals[dst_field] = record[src_col]

        # Remove None values
        partner_vals = {k: v for k, v in partner_vals.items() if v is not None}

        try:
            new_partner = env['res.partner'].with_context(
                tracking_disable=True,
                mail_create_nolog=True,
                mail_notrack=True,
            ).create(partner_vals)
            old_to_new[old_id] = new_partner.id
        except Exception as e:
            _logger.error(
                "Failed to migrate education.parent %s (%s): %s",
                old_id, record.get('name'), str(e))

    _logger.info("Migrated %d guardian records", len(old_to_new))

    if not old_to_new:
        _logger.info("No records migrated, skipping FK updates")
        return

    # Update FK references in education_student (father_id, mother_id)
    if _table_exists(cr, 'education_student'):
        for old_id, new_id in old_to_new.items():
            cr.execute("""
                UPDATE education_student
                SET father_id = %s WHERE father_id = %s
            """, (new_id, old_id))
            cr.execute("""
                UPDATE education_student
                SET mother_id = %s WHERE mother_id = %s
            """, (new_id, old_id))

    # Update FK in education_kids_area_booking (parent_id)
    if _table_exists(cr, 'education_kids_area_booking'):
        for old_id, new_id in old_to_new.items():
            cr.execute("""
                UPDATE education_kids_area_booking
                SET parent_id = %s WHERE parent_id = %s
            """, (new_id, old_id))

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

    env.cr.commit()
    _logger.info("Guardian migration completed successfully")
