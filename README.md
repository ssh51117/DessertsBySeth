# TODO
## Frontend:


## Backend:
  3. Stripe integration — the checkout view is more complex and depends on the basic views working first
    - check rollback setup everywhere
    - check stripe webhook
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

## Stripe Integration
Workflow:                                         
                                                    
  1. Customer submits order → PreorderView.post()   
  creates a Preorder with status PENDING, then calls
   Stripe API to create a PaymentIntent, saves the  
  stripe_payment_intent_id, and returns the         
  client_secret to the frontend                     
  2. Frontend uses Stripe.js to render the payment  
  form and collect card details using the           
  client_secret
  3. Customer submits payment → Stripe processes it 
  4. Stripe sends a webhook event
  (payment_intent.succeeded or                      
  payment_intent.payment_failed) to your backend
  5. Webhook handler updates Preorder.status to     
  CONFIRMED or CANCELLED
  6. Frontend polls GET /api/orders/<id>/status/
  until status changes, then shows confirmation     
   
  Files needed:                                     
                  
  - views.py — update PreorderView.post() to create 
  the PaymentIntent and return client_secret; add a
  new StripeWebhookView to handle incoming webhook  
  events          
  - urls.py — add route for the webhook endpoint
  - settings.py — add STRIPE_SECRET_KEY and
  STRIPE_WEBHOOK_SECRET as environment variables    
  - requirements.txt — add the stripe package
                                                    
  The webhook secret is separate from the API key — 
  Stripe uses it to sign webhook payloads so you can
   verify they're genuinely from Stripe and not     
  spoofed.        

Stripe Docs to Read                                                                                                                 
                                                                                                                                      
  Start here:                                                                                                                         
  - Stripe Quickstart (Python) — end-to-end overview                                                                                  
  - Payment Intents API — the core object you'll use                                                                                  
                                                                                                                                      
  Your specific use case (preorders = pay now, fulfill later):                                                                        
  - Capture later / separate auth & capture — lets you authorize a card at order time and capture when you fulfill, or just charge    
  immediately                                                                                                                         
  - Webhooks — critical — how Stripe notifies your backend that payment succeeded/failed                                              
                                                                                                                                      
  Django integration:                                                                                                                 
  - stripe Python library — the official SDK                                                                                          
  - Fulfillment via webhooks guide — the canonical pattern for order confirmation                                                     
                                                                                                                                      
  ---                                                                                                                                 
  What You'll Need to Build
                                                                                                                                      
  1. POST /orders/ — creates a Stripe PaymentIntent, returns client_secret to frontend
  2. POST /webhooks/stripe/ — listens for payment_intent.succeeded to confirm the order                                               
  3. Store stripe_payment_intent_id on your PreorderItem model                                                                        
                                                                                                                                      
  Install                                                                                                                             
                                                                                                                                      
  pip install stripe                                                                                                                  
                  
  Then set STRIPE_SECRET_KEY and STRIPE_WEBHOOK_SECRET in your environment/settings.

  ---
  The webhook endpoint is the most important part to get right — Stripe's webhook guide covers verifying signatures (use
  stripe.Webhook.construct_event) to prevent spoofed requests.    

# Summary
next.js
django REST
postrgreSQL

host on aws
payments with stripe