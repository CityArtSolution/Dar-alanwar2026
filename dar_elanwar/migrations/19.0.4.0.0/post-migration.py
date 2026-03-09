# -*- coding: utf-8 -*-
import logging
from odoo import api, SUPERUSER_ID

_logger = logging.getLogger(__name__)

# Tables with student_id FK that need updating (table_name, column_name)
STUDENT_FK_TABLES = [
    ('education_sibling', 'student_id'),
    ('education_sibling', 'enrolled_student_id'),
    ('education_authorized_pickup', 'student_id'),
    ('education_student_note', 'student_id'),
    ('education_student_archive', 'student_id'),
    ('education_student_subscription', 'student_id'),
    ('education_attendance_line', 'student_id'),
    ('education_student_evaluation', 'student_id'),
    ('education_student_transport', 'student_id'),
    ('education_student_homework', 'student_id'),
    ('education_stock_out_line', 'student_id'),
    ('education_payment_receipt', 'student_id'),
    ('education_study_plan', 'student_id'),
    ('education_financial_plan', 'student_id'),
    ('education_email_log', 'student_id'),
    ('education_content_student_access', 'student_id'),
    ('education_content_enrollment', 'student_id'),
    ('education_kids_area_booking', 'student_id'),
    ('education_kids_area_attendance', 'student_id'),
    ('education_transaction', 'student_id'),
    ('education_admission_application', 'student_id'),
]

# Many2many relation table
M2M_TABLES = [
    ('education_message_student_rel', 'student_id'),
]


def _table_exists(cr, table_name):
    cr.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_name = %s
        )
    """, (table_name,))
    return cr.fetchone()[0]


def _column_exists(cr, table_name, column_name):
    cr.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.columns
            WHERE table_name = %s AND column_name = %s
        )
    """, (table_name, column_name))
    return cr.fetchone()[0]


def migrate(cr, version):
    """Migrate education.student records to res.partner with is_student=True."""
    env = api.Environment(cr, SUPERUSER_ID, {})
    _logger.info("Starting student migration from education.student to res.partner")

    if not _table_exists(cr, 'education_student'):
        _logger.info("education_student table does not exist, skipping migration")
        return

    # Count records
    cr.execute("SELECT COUNT(*) FROM education_student")
    total = cr.fetchone()[0]
    _logger.info("Found %d education_student records to migrate", total)

    if total == 0:
        _logger.info("No student records to migrate")
        return

    # Determine available columns (photo may not exist as column if attachment=True)
    cr.execute("""
        SELECT column_name FROM information_schema.columns
        WHERE table_name = 'education_student'
    """)
    available_columns = {row[0] for row in cr.fetchall()}

    # Build SELECT columns list (skip photo — stored in ir.attachment)
    select_cols = [
        'id', 'name', 'phone', 'active',
    ]
    optional_cols = [
        'code', 'arabic_name', 'birthdate', 'gender', 'admission_time',
        'birth_order', 'religion', 'birth_place',
        'department_id', 'class_id', 'academic_year_id',
        'enrollment_date', 'enrollment_source_id', 'period', 'branch_id',
        'city_id', 'blood_type', 'allergies', 'medical_notes',
        'state', 'father_id', 'mother_id',
        'address', 'nationality', 'national_id', 'notes',
    ]
    for col in optional_cols:
        if col in available_columns:
            select_cols.append(col)

    cr.execute("SELECT %s FROM education_student" % ', '.join(select_cols))
    student_records = cr.fetchall()
    columns = [desc[0] for desc in cr.description]

    old_to_new = {}  # old student ID -> new partner ID
    migrated = 0
    errors = 0

    for row in student_records:
        record = dict(zip(columns, row))
        old_id = record['id']

        try:
            partner_vals = {
                'name': record.get('name') or 'Unknown Student',
                'phone': record.get('phone'),
                'active': record.get('active', True),
                'is_student': True,
            }

            # Student-specific fields
            field_map = {
                'code': 'code',
                'arabic_name': 'arabic_name',
                'birthdate': 'birthdate',
                'gender': 'gender',
                'admission_time': 'admission_time',
                'birth_order': 'birth_order',
                'religion': 'religion',
                'birth_place': 'birth_place',
                'department_id': 'department_id',
                'class_id': 'class_id',
                'academic_year_id': 'academic_year_id',
                'enrollment_date': 'enrollment_date',
                'enrollment_source_id': 'enrollment_source_id',
                'period': 'period',
                'branch_id': 'branch_id',
                'blood_type': 'blood_type',
                'allergies': 'allergies',
                'medical_notes': 'medical_notes',
                # father_id and mother_id already point to res.partner
                # (updated by guardian migration 19.0.3.0.0)
                'father_id': 'father_id',
                'mother_id': 'mother_id',
            }

            for old_field, new_field in field_map.items():
                val = record.get(old_field)
                if val is not None:
                    # blood_type stored as uppercase in DB, selection expects lowercase
                    if old_field == 'blood_type' and isinstance(val, str):
                        val = val.lower()
                    # period: map legacy 'evening' to 'afternoon'
                    if old_field == 'period' and val == 'evening':
                        val = 'afternoon'
                    partner_vals[new_field] = val

            # Renamed fields
            if 'state' in record and record['state'] is not None:
                partner_vals['student_state'] = record['state']

            if 'city_id' in record and record['city_id'] is not None:
                partner_vals['student_city_id'] = record['city_id']

            if 'nationality' in record and record['nationality'] is not None:
                partner_vals['country_id'] = record['nationality']

            if 'national_id' in record and record['national_id'] is not None:
                partner_vals['id_number'] = record['national_id']

            if 'address' in record and record['address'] is not None:
                partner_vals['street'] = str(record['address'])[:256]

            if 'notes' in record and record['notes'] is not None:
                partner_vals['comment'] = '<p>%s</p>' % (record['notes'] or '')

            # Remove None values
            partner_vals = {k: v for k, v in partner_vals.items() if v is not None}

            new_partner = env['res.partner'].with_context(
                tracking_disable=True,
                mail_create_nolog=True,
                mail_notrack=True,
            ).create(partner_vals)
            old_to_new[old_id] = new_partner.id
            migrated += 1

            if migrated % 100 == 0:
                _logger.info("Migrated %d/%d student records...", migrated, total)
                env.cr.commit()

        except Exception as e:
            _logger.error(
                "Failed to migrate education.student %s (%s): %s",
                old_id, record.get('name'), str(e))
            errors += 1

    _logger.info(
        "Student record migration: %d migrated, %d errors out of %d total",
        migrated, errors, total)

    # Migrate photo attachments (stored in ir.attachment)
    _logger.info("Migrating student photo attachments...")
    for old_id, new_id in old_to_new.items():
        cr.execute("""
            UPDATE ir_attachment
            SET res_model = 'res.partner', res_id = %s,
                res_field = 'image_1920'
            WHERE res_model = 'education.student'
              AND res_id = %s
              AND res_field = 'photo'
        """, (new_id, old_id))

    # Also migrate any other attachments on the old student records
    for old_id, new_id in old_to_new.items():
        cr.execute("""
            UPDATE ir_attachment
            SET res_model = 'res.partner', res_id = %s
            WHERE res_model = 'education.student'
              AND res_id = %s
        """, (new_id, old_id))

    # Update FK references in related tables
    _logger.info("Updating FK references in related tables...")
    for table_name, column_name in STUDENT_FK_TABLES:
        if not _table_exists(cr, table_name):
            _logger.info("Table %s does not exist, skipping", table_name)
            continue
        if not _column_exists(cr, table_name, column_name):
            _logger.info("Column %s.%s does not exist, skipping",
                         table_name, column_name)
            continue

        updated = 0
        for old_id, new_id in old_to_new.items():
            cr.execute(
                "UPDATE %s SET %s = %%s WHERE %s = %%s" % (
                    table_name, column_name, column_name),
                (new_id, old_id))
            updated += cr.rowcount

        if updated:
            _logger.info("Updated %d rows in %s.%s",
                         updated, table_name, column_name)

    # Update M2M relation tables
    for table_name, column_name in M2M_TABLES:
        if not _table_exists(cr, table_name):
            _logger.info("M2M table %s does not exist, skipping", table_name)
            continue

        updated = 0
        for old_id, new_id in old_to_new.items():
            cr.execute(
                "UPDATE %s SET %s = %%s WHERE %s = %%s" % (
                    table_name, column_name, column_name),
                (new_id, old_id))
            updated += cr.rowcount

        if updated:
            _logger.info("Updated %d rows in M2M table %s.%s",
                         updated, table_name, column_name)

    # Migrate mail.message records
    _logger.info("Migrating mail.message records...")
    msg_count = 0
    for old_id, new_id in old_to_new.items():
        cr.execute("""
            UPDATE mail_message
            SET model = 'res.partner', res_id = %s
            WHERE model = 'education.student' AND res_id = %s
        """, (new_id, old_id))
        msg_count += cr.rowcount
    _logger.info("Migrated %d mail.message records", msg_count)

    # Migrate mail.activity records
    if _column_exists(cr, 'mail_activity', 'res_model'):
        _logger.info("Migrating mail.activity records...")
        act_count = 0
        for old_id, new_id in old_to_new.items():
            cr.execute("""
                UPDATE mail_activity
                SET res_model = 'res.partner', res_id = %s
                WHERE res_model = 'education.student' AND res_id = %s
            """, (new_id, old_id))
            act_count += cr.rowcount
        _logger.info("Migrated %d mail.activity records", act_count)

    # Migrate mail.followers
    if _table_exists(cr, 'mail_followers'):
        _logger.info("Migrating mail.followers records...")
        fol_count = 0
        for old_id, new_id in old_to_new.items():
            cr.execute("""
                UPDATE mail_followers
                SET res_model = 'res.partner', res_id = %s
                WHERE res_model = 'education.student' AND res_id = %s
            """, (new_id, old_id))
            fol_count += cr.rowcount
        _logger.info("Migrated %d mail.followers records", fol_count)

    # Create partial unique index for student code
    _logger.info("Creating partial unique index for student code...")
    # Drop any existing index first (may have duplicates from prior partial migration)
    cr.execute("DROP INDEX IF EXISTS education_student_code_unique")
    # Remove duplicate codes from any previously failed migration attempts
    cr.execute("""
        UPDATE res_partner SET code = NULL
        WHERE id NOT IN (
            SELECT MIN(id) FROM res_partner
            WHERE is_student = TRUE AND code IS NOT NULL
            GROUP BY code
        )
        AND is_student = TRUE AND code IS NOT NULL
    """)
    try:
        cr.execute("""
            CREATE UNIQUE INDEX education_student_code_unique
            ON res_partner (code)
            WHERE is_student = TRUE AND code IS NOT NULL
        """)
    except Exception as e:
        _logger.warning("Could not create unique index for student code: %s", str(e))

    env.cr.commit()

    # Log migration summary
    _logger.info("=" * 60)
    _logger.info("STUDENT MIGRATION SUMMARY")
    _logger.info("=" * 60)
    _logger.info("Total education.student records: %d", total)
    _logger.info("Successfully migrated: %d", migrated)
    _logger.info("Errors: %d", errors)
    _logger.info("ID mapping entries: %d", len(old_to_new))
    _logger.info("=" * 60)
    _logger.info("Student migration completed successfully")
