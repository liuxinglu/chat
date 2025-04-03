from app.database import db
from app.model.models import Ticket


class TicketService():

    ticket = None

    def add_ticket(self, ticket=None, index=None, message=None, reply=None, good_bad=None, user_id=None):
        self.ticket = Ticket(index=index, user_id=user_id) if self.ticket == None else ticket


        if message != None:
            self.ticket.message = message

        if reply != None:
            self.ticket.reply = reply

        if good_bad != None:
            self.ticket.good1_bad0 = good_bad
        db.session.add(self.ticket)
        db.session.commit()

    def get_ticket_history(self, user_id):
        tickets = Ticket.query.filter_by(user_id=user_id).all()
        return [{'ticketid': t.id, 'question': t.message, 'reply': t.reply, 'goodorbad': t.good1_bad0} for t in tickets]

    def get_ticket_by_index(self, index):
        ticket = Ticket.query.filter_by(index=index).first()
        return ticket