from pathlib import Path
path = Path('backend/migrations/versions/20251001_01_create_customers_bookings.py')
text = path.read_text()
text = text.replace(
    '    sa.Column("status", booking_status_enum, nullable=False, server_default="pending"),\n',
    '    sa.Column("status", sa.Enum("pending", "approved", "declined", "cancelled", name="booking_status", create_type=False), nullable=False, server_default="pending"),\n'
)
path.write_text(text)
