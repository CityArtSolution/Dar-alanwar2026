# -*- coding: utf-8 -*-

import logging
from werkzeug.security import generate_password_hash

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    """Auto-create portal users for existing guardians with phone numbers.

    Uses their id_number (national ID) as the initial password, hashed with werkzeug.
    Guardians without a phone number are skipped.
    """
    _logger.info('Creating portal user accounts for existing guardians...')

    # No unique indexes — Python @api.constrains handles validation

    # Find all guardians with a phone number who don't already have a portal user
    cr.execute("""
        SELECT rp.id, rp.phone, rp.id_number
        FROM res_partner rp
        WHERE rp.is_guardian = TRUE
          AND rp.phone IS NOT NULL
          AND rp.phone != ''
          AND rp.active = TRUE
          AND NOT EXISTS (
              SELECT 1 FROM dar_portal_user dpu
              WHERE dpu.partner_id = rp.id
          )
    """)

    guardians = cr.fetchall()
    created = 0
    skipped = 0

    for partner_id, phone, id_number in guardians:
        username = phone.strip()
        raw_password = id_number if id_number else str(partner_id)
        password_hash = generate_password_hash(raw_password)

        # Check if username already taken (duplicate phone numbers)
        cr.execute(
            "SELECT 1 FROM dar_portal_user WHERE username = %s",
            (username,)
        )
        if cr.fetchone():
            _logger.info(
                'Skipping partner %s: username %s already exists',
                partner_id, username
            )
            skipped += 1
            continue

        cr.execute("""
            INSERT INTO dar_portal_user
                (partner_id, username, password_hash, is_active,
                 user_type, login_count, create_date, write_date, create_uid, write_uid)
            VALUES
                (%s, %s, %s, TRUE, 'parent', 0, NOW(), NOW(), 1, 1)
        """, (partner_id, username, password_hash))
        created += 1

    _logger.info(
        'Created %d portal user accounts out of %d guardians (%d skipped).',
        created, len(guardians), skipped
    )

    # Update stored computed fields on res_partner
    cr.execute("""
        UPDATE res_partner rp
        SET has_portal_user = TRUE,
            portal_user_id = dpu.id
        FROM dar_portal_user dpu
        WHERE dpu.partner_id = rp.id
    """)
