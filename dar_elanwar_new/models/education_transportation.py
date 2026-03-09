from odoo import models, fields, api


class EducationVehicle(models.Model):
    _name = 'education.vehicle'
    _description = 'Transportation Vehicle'

    name = fields.Char(string='Vehicle Name', required=True)
    plate_number = fields.Char(string='Plate Number', required=True)
    vehicle_type = fields.Selection([
        ('bus', 'Bus'),
        ('van', 'Van'),
        ('car', 'Car'),
    ], string='Type', default='bus')
    capacity = fields.Integer(string='Capacity')
    driver_id = fields.Many2one('education.employee', string='Driver')
    supervisor_id = fields.Many2one('education.employee', string='Supervisor')
    active = fields.Boolean(default=True)
    route_ids = fields.One2many('education.route', 'vehicle_id',
                                 string='Routes')


class EducationRoute(models.Model):
    _name = 'education.route'
    _description = 'Transportation Route'

    name = fields.Char(string='Route Name', required=True)
    vehicle_id = fields.Many2one('education.vehicle', string='Vehicle',
                                  required=True)
    route_type = fields.Selection([
        ('morning', 'Morning Pickup'),
        ('afternoon', 'Afternoon Drop-off'),
        ('both', 'Both'),
    ], string='Type', default='both')
    stop_ids = fields.One2many('education.route.stop', 'route_id',
                                string='Stops')
    student_ids = fields.Many2many('education.student',
                                     'route_student_rel',
                                     'route_id', 'student_id',
                                     string='Students')
    active = fields.Boolean(default=True)


class EducationRouteStop(models.Model):
    _name = 'education.route.stop'
    _description = 'Route Stop'
    _order = 'sequence'

    route_id = fields.Many2one('education.route', string='Route',
                                required=True, ondelete='cascade')
    sequence = fields.Integer(string='Order', default=10)
    name = fields.Char(string='Stop Name', required=True)
    address = fields.Text(string='Address')
    pickup_time = fields.Float(string='Pickup Time')
    dropoff_time = fields.Float(string='Drop-off Time')


class EducationTransportationSubscription(models.Model):
    _name = 'education.transportation.subscription'
    _description = 'Transportation Subscription'

    student_id = fields.Many2one('education.student', string='Student',
                                  required=True)
    route_id = fields.Many2one('education.route', string='Route',
                                required=True)
    stop_id = fields.Many2one('education.route.stop', string='Pickup Stop',
                               domain="[('route_id', '=', route_id)]")
    subscription_type = fields.Selection([
        ('one_way', 'One Way'),
        ('two_way', 'Two Way'),
    ], string='Type', default='two_way')
    monthly_fee = fields.Float(string='Monthly Fee')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    active = fields.Boolean(default=True)
