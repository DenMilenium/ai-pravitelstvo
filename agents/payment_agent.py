#!/usr/bin/env python3
"""
💳 Payment-Agent
Payment Integration агент

Создаёт:
- Платёжные интеграции
- Stripe/PayPal
- Подписки
- Инвойсы
"""

import argparse
from pathlib import Path
from typing import Dict


class PaymentAgent:
    """
    💳 Payment-Agent
    
    Специализация: Payment Integration
    Технологии: Stripe, PayPal, Webhooks
    """
    
    NAME = "💳 Payment-Agent"
    ROLE = "Payment Developer"
    EXPERTISE = ["Stripe", "PayPal", "Subscriptions", "Invoices", "Webhooks"]
    
    def process_request(self, request: str) -> Dict[str, str]:
        files = {}
        
        files["stripe-integration.js"] = """const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

class PaymentService {
  constructor() {
    this.stripe = stripe;
  }
  
  // Create a customer
  async createCustomer(email, name, metadata = {}) {
    return await this.stripe.customers.create({
      email,
      name,
      metadata
    });
  }
  
  // Create a payment intent
  async createPaymentIntent(amount, currency = 'usd', customerId = null, metadata = {}) {
    const params = {
      amount: Math.round(amount * 100), // Convert to cents
      currency,
      automatic_payment_methods: { enabled: true },
      metadata
    };
    
    if (customerId) {
      params.customer = customerId;
    }
    
    return await this.stripe.paymentIntents.create(params);
  }
  
  // Create a subscription
  async createSubscription(customerId, priceId, metadata = {}) {
    return await this.stripe.subscriptions.create({
      customer: customerId,
      items: [{ price: priceId }],
      payment_behavior: 'default_incomplete',
      expand: ['latest_invoice.payment_intent'],
      metadata
    });
  }
  
  // Cancel subscription
  async cancelSubscription(subscriptionId) {
    return await this.stripe.subscriptions.cancel(subscriptionId);
  }
  
  // Create checkout session
  async createCheckoutSession(customerId, lineItems, successUrl, cancelUrl, mode = 'payment') {
    return await this.stripe.checkout.sessions.create({
      customer: customerId,
      line_items: lineItems,
      mode, // 'payment', 'subscription', or 'setup'
      success_url: successUrl,
      cancel_url: cancelUrl,
      billing_address_collection: 'required',
      allow_promotion_codes: true
    });
  }
  
  // Create a product
  async createProduct(name, description, metadata = {}) {
    return await this.stripe.products.create({
      name,
      description,
      metadata
    });
  }
  
  // Create a price for a product
  async createPrice(productId, unitAmount, currency = 'usd', interval = null) {
    const params = {
      product: productId,
      unit_amount: Math.round(unitAmount * 100),
      currency
    };
    
    if (interval) {
      params.recurring = { interval }; // 'month' or 'year'
    }
    
    return await this.stripe.prices.create(params);
  }
  
  // Handle webhook events
  async handleWebhook(payload, signature, webhookSecret) {
    try {
      const event = this.stripe.webhooks.constructEvent(
        payload,
        signature,
        webhookSecret
      );
      
      switch (event.type) {
        case 'payment_intent.succeeded':
          await this.handlePaymentSuccess(event.data.object);
          break;
          
        case 'payment_intent.payment_failed':
          await this.handlePaymentFailure(event.data.object);
          break;
          
        case 'customer.subscription.created':
          await this.handleSubscriptionCreated(event.data.object);
          break;
          
        case 'customer.subscription.deleted':
          await this.handleSubscriptionCancelled(event.data.object);
          break;
          
        case 'invoice.payment_succeeded':
          await this.handleInvoicePaymentSucceeded(event.data.object);
          break;
          
        default:
          console.log(`Unhandled event type: ${event.type}`);
      }
      
      return { received: true };
    } catch (error) {
      console.error('Webhook error:', error);
      throw error;
    }
  }
  
  // Event handlers
  async handlePaymentSuccess(paymentIntent) {
    console.log('Payment succeeded:', paymentIntent.id);
    // Update database, send confirmation email, etc.
  }
  
  async handlePaymentFailure(paymentIntent) {
    console.log('Payment failed:', paymentIntent.id);
    // Log failure, notify user, etc.
  }
  
  async handleSubscriptionCreated(subscription) {
    console.log('Subscription created:', subscription.id);
    // Update user subscription status
  }
  
  async handleSubscriptionCancelled(subscription) {
    console.log('Subscription cancelled:', subscription.id);
    // Update user subscription status
  }
  
  async handleInvoicePaymentSucceeded(invoice) {
    console.log('Invoice payment succeeded:', invoice.id);
    // Send receipt, update records
  }
}

module.exports = PaymentService;
"""
        
        files["paypal-integration.js"] = """const paypal = require('@paypal/checkout-server-sdk');

class PayPalService {
  constructor() {
    const environment = process.env.NODE_ENV === 'production'
      ? new paypal.core.LiveEnvironment(
          process.env.PAYPAL_CLIENT_ID,
          process.env.PAYPAL_CLIENT_SECRET
        )
      : new paypal.core.SandboxEnvironment(
          process.env.PAYPAL_CLIENT_ID,
          process.env.PAYPAL_CLIENT_SECRET
        );
    
    this.client = new paypal.core.PayPalHttpClient(environment);
  }
  
  // Create an order
  async createOrder(amount, currency = 'USD', description = '') {
    const request = new paypal.orders.OrdersCreateRequest();
    request.prefer('return=representation');
    request.requestBody({
      intent: 'CAPTURE',
      purchase_units: [{
        amount: {
          currency_code: currency,
          value: amount.toFixed(2)
        },
        description
      }],
      application_context: {
        return_url: process.env.PAYPAL_RETURN_URL,
        cancel_url: process.env.PAYPAL_CANCEL_URL
      }
    });
    
    const response = await this.client.execute(request);
    return response.result;
  }
  
  // Capture payment
  async capturePayment(orderId) {
    const request = new paypal.orders.OrdersCaptureRequest(orderId);
    request.prefer('return=representation');
    
    const response = await this.client.execute(request);
    return response.result;
  }
  
  // Get order details
  async getOrder(orderId) {
    const request = new paypal.orders.OrdersGetRequest(orderId);
    const response = await this.client.execute(request);
    return response.result;
  }
  
  // Create subscription plan
  async createSubscriptionPlan(productName, description, amount, frequency = 'MONTH') {
    // Create product
    const productRequest = new paypal.catalogs.ProductsCreateRequest();
    productRequest.requestBody({
      name: productName,
      description,
      type: 'SERVICE',
      category: 'SOFTWARE'
    });
    
    const productResponse = await this.client.execute(productRequest);
    const productId = productResponse.result.id;
    
    // Create plan
    const planRequest = new paypal.billing.PlansCreateRequest();
    planRequest.requestBody({
      product_id: productId,
      name: `${productName} Plan`,
      description: `${frequency} subscription`,
      billing_cycles: [{
        frequency: { interval_unit: frequency, interval_count: 1 },
        tenure_type: 'REGULAR',
        sequence: 1,
        total_cycles: 0,
        pricing_scheme: {
          fixed_price: {
            value: amount.toFixed(2),
            currency_code: 'USD'
          }
        }
      }],
      payment_preferences: {
        auto_bill_outstanding: true,
        setup_fee_failure_action: 'CONTINUE',
        payment_failure_threshold: 3
      }
    });
    
    const planResponse = await this.client.execute(planRequest);
    return planResponse.result;
  }
}

module.exports = PayPalService;
"""
        
        files["subscription-manager.js"] = """class SubscriptionManager {
  constructor(paymentService) {
    this.payment = paymentService;
    this.plans = new Map();
  }
  
  // Define subscription plans
  definePlans() {
    this.plans.set('basic', {
      id: 'price_basic',
      name: 'Basic',
      price: 9.99,
      interval: 'month',
      features: ['5 projects', '10GB storage', 'Email support']
    });
    
    this.plans.set('pro', {
      id: 'price_pro',
      name: 'Pro',
      price: 29.99,
      interval: 'month',
      features: ['Unlimited projects', '100GB storage', 'Priority support', 'API access']
    });
    
    this.plans.set('enterprise', {
      id: 'price_enterprise',
      name: 'Enterprise',
      price: 99.99,
      interval: 'month',
      features: ['Everything in Pro', 'Unlimited storage', 'Dedicated support', 'Custom integrations', 'SLA']
    });
  }
  
  // Get plan details
  getPlan(planId) {
    return this.plans.get(planId);
  }
  
  // Get all plans
  getAllPlans() {
    return Array.from(this.plans.entries()).map(([id, plan]) => ({
      id,
      ...plan
    }));
  }
  
  // Subscribe user to plan
  async subscribe(userId, planId, paymentMethod) {
    const plan = this.getPlan(planId);
    if (!plan) throw new Error('Invalid plan');
    
    // Create subscription in payment provider
    const subscription = await this.payment.createSubscription(
      userId,
      plan.id
    );
    
    return {
      subscriptionId: subscription.id,
      status: subscription.status,
      currentPeriodEnd: subscription.current_period_end,
      plan: plan
    };
  }
  
  // Cancel subscription
  async cancel(subscriptionId) {
    return await this.payment.cancelSubscription(subscriptionId);
  }
  
  // Change plan
  async changePlan(subscriptionId, newPlanId) {
    const newPlan = this.getPlan(newPlanId);
    if (!newPlan) throw new Error('Invalid plan');
    
    // Update subscription with new price
    return await this.payment.updateSubscription(subscriptionId, {
      items: [{ price: newPlan.id }]
    });
  }
}

module.exports = SubscriptionManager;
"""
        
        return files


def main():
    parser = argparse.ArgumentParser(description="💳 Payment-Agent — Payments")
    parser.add_argument("request", nargs="?", help="Что создать")
    parser.add_argument("--output", "-o", help="Папка для сохранения")
    
    args = parser.parse_args()
    
    agent = PaymentAgent()
    
    if args.request:
        print(f"💳 {agent.NAME} создаёт: {args.request}")
        files = agent.process_request(args.request)
        
        if args.output:
            output_dir = Path(args.output)
            output_dir.mkdir(parents=True, exist_ok=True)
            for filename, content in files.items():
                filepath = output_dir / filename
                filepath.write_text(content, encoding="utf-8")
                print(f"✅ {filename}")
        else:
            for filename, content in files.items():
                print(f"\n{'='*50}")
                print(f"📄 {filename}")
                print('='*50)
                print(content[:500] + "..." if len(content) > 500 else content)
    else:
        print(f"💳 {agent.NAME}")
        print(f"Роль: {agent.ROLE}")


if __name__ == "__main__":
    main()
