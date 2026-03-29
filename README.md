# TODO
## Frontend:


## Backend:
  3. Stripe integration — the checkout view is more complex and depends on the basic views working first
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

## Stripe
Stripe Frontend Plan                                                                                                                
                                                                                                                                      
  1. Cart State Management                                                                                                            
                                                                                                                                      
      - cartprovider wraps children in the layout, global cart state
      - stripeprovider - used only on cart/checkout page to wrap the stripe stuff to make it client
      - checkoutform lives inside stripeprovder, renders the payment element

                                                                                                                                      
  2. Preorder Flow — Submit Order to Backend                                                                                          
  
  On checkout, POST the cart contents to /api/preorders/ and get back a client_secret and order ID. Store the order ID (e.g. in state 
  or a cookie) so you can poll the status later.
                                                                                                                                      
  3. Render the Stripe Payment Element                                                                                                
  
  Wrap the checkout section in Stripe's <Elements> provider (from @stripe/react-stripe-js) using the client_secret from step 2. Render
   <PaymentElement> inside it — this handles card input, Apple Pay, Google Pay, etc. automatically.
                                                                                                                                      
  4. Handle Payment Submission

  On form submit, call stripe.confirmPayment() with a return_url pointing to a confirmation page. Stripe redirects there after the    
  payment attempt.
                                                                                                                                      
  5. Confirmation Page

  At the return_url, read the payment_intent_client_secret query param that Stripe appends. Poll GET /api/preorders/<id>/status/ until
   the status is CONFIRMED (updated by your webhook), then show a success message.
                                                                                                                                      
  ---             
  Resources
           
  - Stripe.js + React setup: https://docs.stripe.com/stripe-js/react
  - PaymentElement (the all-in-one UI component): https://docs.stripe.com/payments/payment-element                                    
  - confirmPayment() + redirect flow: https://docs.stripe.com/js/payment_intents/confirm_payment                                      
  - Testing with the Stripe CLI: https://docs.stripe.com/stripe-cli                                                                   
  - Test card numbers: https://docs.stripe.com/testing#cards      

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
  CONFIRMED or CANCELED
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