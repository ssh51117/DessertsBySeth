# TODO
## Frontend:
- make loading better
- make other pages
- make buttons clickable

## Backend:
  1. Views + URLs — wire up the basic endpoints so the API actually responds to requests
  2. Validation — add validate() methods to serializers as you implement each view, since you'll know exactly what needs checking
  3. Stripe integration — the checkout view is more complex and depends on the basic views working first
  4. Celery + email — async tasks for notifications, done last since they don't block the core functionality

# Frontend
requirements:
- landing page
- menu
- ordering
- schedule
- contact
- recipes maybe
## pages:
customer: 
- landing
- menu
- cart
- checkout
- contact
- tracking
- about
admin
- add/edit products
- update inventory
- view orders
- mark orders completed
# Backend
need:
- data store of orders
- payment processing
- email / text reminders

# Summary
next.js
django REST
postrgreSQL

host on aws
payments with stripe