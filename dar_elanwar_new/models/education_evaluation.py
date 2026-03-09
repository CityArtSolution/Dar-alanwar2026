from odoo import models, fields, api


class EducationEvaluationTemplate(models.Model):
    _name = 'education.evaluation.template'
    _description = 'Evaluation Template'

    name = fields.Char(string='Template Name', required=True)
    code = fields.Char(string='Code')
    department_id = fields.Many2one('education.department', string='Department')
    subject_id = fields.Many2one('education.subject', string='Subject')
    question_ids = fields.One2many('education.evaluation.question',
                                    'template_id', string='Questions')
    active = fields.Boolean(default=True)


class EducationEvaluationQuestion(models.Model):
    _name = 'education.evaluation.question'
    _description = 'Evaluation Question'
    _order = 'sequence'

    template_id = fields.Many2one('education.evaluation.template',
                                    string='Template', required=True,
                                    ondelete='cascade')
    sequence = fields.Integer(string='Sequence', default=10)
    question = fields.Text(string='Question', required=True)
    scale_id = fields.Many2one('education.grade.scale', string='Grade Scale')
    is_required = fields.Boolean(string='Required', default=True)


class EducationEvaluationGoal(models.Model):
    _name = 'education.evaluation.goal'
    _description = 'Evaluation Goal'
    _inherit = ['mail.thread']
    _order = 'date desc'

    name = fields.Char(string='Goal Name', required=True, tracking=True)
    date = fields.Date(string='Date', default=fields.Date.today)
    template_id = fields.Many2one('education.evaluation.template',
                                    string='Template')
    class_id = fields.Many2one('education.class', string='Class')
    teacher_id = fields.Many2one('education.employee', string='Teacher',
                                  domain=[('is_teacher', '=', True)])
    is_shared = fields.Boolean(string='Shared Goal', default=False)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ], string='Status', default='draft', tracking=True)
    description = fields.Text(string='Description')

    evaluation_ids = fields.One2many('education.student.evaluation',
                                      'goal_id', string='Evaluations')
    evaluation_count = fields.Integer(compute='_compute_evaluation_count',
                                       string='Evaluations')
    completion_rate = fields.Float(compute='_compute_completion_rate',
                                    string='Completion %')

    def _compute_evaluation_count(self):
        for rec in self:
            rec.evaluation_count = len(rec.evaluation_ids)

    def _compute_completion_rate(self):
        for rec in self:
            total = len(rec.evaluation_ids)
            completed = len(rec.evaluation_ids.filtered('is_completed'))
            rec.completion_rate = (completed / total * 100) if total else 0.0

    def action_start(self):
        self.write({'state': 'in_progress'})

    def action_complete(self):
        self.write({'state': 'completed'})


class EducationStudentEvaluation(models.Model):
    _name = 'education.student.evaluation'
    _description = 'Student Evaluation'

    goal_id = fields.Many2one('education.evaluation.goal', string='Goal',
                               required=True, ondelete='cascade')
    student_id = fields.Many2one('education.student', string='Student',
                                  required=True)
    evaluator_id = fields.Many2one('res.users', string='Evaluator',
                                    default=lambda self: self.env.user)
    is_completed = fields.Boolean(string='Completed', default=False)
    completion_date = fields.Date(string='Completion Date')
    notes = fields.Text(string='Notes')

    answer_ids = fields.One2many('education.evaluation.answer',
                                  'evaluation_id', string='Answers')

    def action_mark_complete(self):
        self.write({
            'is_completed': True,
            'completion_date': fields.Date.today(),
        })


class EducationEvaluationAnswer(models.Model):
    _name = 'education.evaluation.answer'
    _description = 'Evaluation Answer'

    evaluation_id = fields.Many2one('education.student.evaluation',
                                     string='Evaluation', required=True,
                                     ondelete='cascade')
    question_id = fields.Many2one('education.evaluation.question',
                                   string='Question', required=True)
    answer_value_id = fields.Many2one('education.grade.scale.value',
                                       string='Answer')
    numeric_answer = fields.Float(string='Numeric Answer')
    notes = fields.Text(string='Notes')
