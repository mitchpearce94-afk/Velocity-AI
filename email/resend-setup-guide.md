# Velocity AI — Resend Email Infrastructure Setup Guide

## Overview

This guide covers the complete setup of Resend (resend.com) as the email service provider for Velocity AI. Resend handles both transactional emails (welcome emails, confirmations) and marketing emails (follow-ups, newsletters).

**Domain:** velocityai.com.au
**Provider:** Resend (resend.com)
**Sending address:** mitchell@velocityai.com.au

---

## 1. Create a Resend Account

1. Navigate to [resend.com](https://resend.com) and click **Get Started**.
2. Sign up using your Velocity AI Google Workspace account or email.
3. Verify your email address via the confirmation link.
4. Select a plan:
   - **Free tier** — 100 emails/day, 3,000 emails/month (suitable for early stage)
   - **Pro** — 50,000 emails/month, custom domains, dedicated IPs (recommended for production)
5. Complete account setup and access the dashboard.

---

## 2. Add the velocityai.com.au Domain

1. In the Resend dashboard, navigate to **Domains** in the left sidebar.
2. Click **Add Domain**.
3. Enter `velocityai.com.au` as the domain.
4. Select the region closest to your audience — choose **Not US** (Sydney/AP region if available, otherwise EU).
5. Click **Add** to generate the required DNS records.

---

## 3. Configure DNS Records

Add the following DNS records to your domain registrar (e.g., Cloudflare, Namecheap, GoDaddy, VentraIP). Resend will provide the exact values in the dashboard — the records below are the types you'll need.

### 3.1 SPF Record

SPF (Sender Policy Framework) authorises Resend to send emails on behalf of velocityai.com.au.

| Type | Host/Name          | Value                                        | TTL  |
|------|--------------------|----------------------------------------------|------|
| TXT  | `@` or blank       | `v=spf1 include:send.resend.com -all`        | 3600 |

> **Note:** If you already have an SPF record (e.g., for Google Workspace), merge them into a single record:
> `v=spf1 include:_spf.google.com include:send.resend.com -all`

### 3.2 DKIM Records

DKIM (DomainKeys Identified Mail) adds a cryptographic signature to outgoing emails. Resend will provide three CNAME records.

| Type  | Host/Name                              | Value (provided by Resend)                    | TTL  |
|-------|----------------------------------------|-----------------------------------------------|------|
| CNAME | `resend._domainkey.velocityai.com.au`  | *(Resend will provide this value)*            | 3600 |
| CNAME | `resend2._domainkey.velocityai.com.au` | *(Resend will provide this value)*            | 3600 |
| CNAME | `resend3._domainkey.velocityai.com.au` | *(Resend will provide this value)*            | 3600 |

> Copy the exact CNAME values from the Resend dashboard. Do not modify them.

### 3.3 DMARC Record

DMARC (Domain-based Message Authentication, Reporting, and Conformance) tells receiving servers what to do with emails that fail SPF/DKIM checks.

| Type | Host/Name | Value                                                          | TTL  |
|------|-----------|----------------------------------------------------------------|------|
| TXT  | `_dmarc`  | `v=DMARC1; p=quarantine; rua=mailto:dmarc@velocityai.com.au`  | 3600 |

**DMARC policy progression:**

1. **Start with `p=none`** — Monitor only, no enforcement. Use this for the first 2–4 weeks.
   ```
   v=DMARC1; p=none; rua=mailto:dmarc@velocityai.com.au
   ```
2. **Move to `p=quarantine`** — Suspicious emails go to spam. Use once reports look clean.
   ```
   v=DMARC1; p=quarantine; rua=mailto:dmarc@velocityai.com.au
   ```
3. **Final: `p=reject`** — Full protection. Failed emails are rejected outright.
   ```
   v=DMARC1; p=reject; rua=mailto:dmarc@velocityai.com.au
   ```

### 3.4 Return-Path / Bounce Domain (Optional)

Resend may also request a return-path CNAME for bounce handling:

| Type  | Host/Name                       | Value (provided by Resend)    | TTL  |
|-------|---------------------------------|-------------------------------|------|
| CNAME | `bounces.velocityai.com.au`     | *(Resend will provide this)*  | 3600 |

### 3.5 Verify DNS Records

1. After adding all DNS records, return to the Resend dashboard.
2. Click **Verify** next to the velocityai.com.au domain.
3. DNS propagation can take up to 48 hours, but typically completes within 1–2 hours.
4. You can check propagation status at [dnschecker.org](https://dnschecker.org).

---

## 4. API Key Setup

### 4.1 Create API Keys

1. In the Resend dashboard, go to **API Keys**.
2. Create separate keys for each environment:

| Key Name                   | Permission    | Use Case                        |
|----------------------------|---------------|----------------------------------|
| `velocity-ai-production`   | Full access   | Production application           |
| `velocity-ai-staging`      | Full access   | Staging/testing environment      |
| `velocity-ai-marketing`    | Sending only  | Marketing campaigns              |

3. Copy each key immediately — they are only shown once.

### 4.2 Store API Keys Securely

**Never commit API keys to version control.**

Store them as environment variables:

```bash
# .env (local development)
RESEND_API_KEY=re_xxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Production — use your hosting provider's secrets manager
# e.g., Vercel, AWS Secrets Manager, Railway, etc.
```

Add `.env` to your `.gitignore`:

```
# .gitignore
.env
.env.local
.env.production
```

### 4.3 Test the API Key

Send a test email via cURL:

```bash
curl -X POST 'https://api.resend.com/emails' \
  -H 'Authorization: Bearer re_xxxxxxxxxxxxxxxxxxxxxxxxxxxx' \
  -H 'Content-Type: application/json' \
  -d '{
    "from": "Mitchell Pearce <mitchell@velocityai.com.au>",
    "to": ["mitchell@velocityai.com.au"],
    "subject": "Resend Test — Velocity AI",
    "html": "<p>If you are reading this, Resend is configured correctly.</p>"
  }'
```

Or using the Resend Node.js SDK:

```javascript
import { Resend } from 'resend';

const resend = new Resend(process.env.RESEND_API_KEY);

const { data, error } = await resend.emails.send({
  from: 'Mitchell Pearce <mitchell@velocityai.com.au>',
  to: ['mitchell@velocityai.com.au'],
  subject: 'Resend Test — Velocity AI',
  html: '<p>If you are reading this, Resend is configured correctly.</p>',
});

if (error) {
  console.error('Send failed:', error);
} else {
  console.log('Email sent:', data.id);
}
```

---

## 5. Webhook Configuration

Webhooks let you track email events (delivered, opened, bounced, etc.) in real time.

### 5.1 Set Up a Webhook Endpoint

Create an endpoint in your application to receive webhook events:

```
POST https://api.velocityai.com.au/webhooks/resend
```

### 5.2 Register the Webhook in Resend

1. Go to **Webhooks** in the Resend dashboard.
2. Click **Add Webhook**.
3. Enter your endpoint URL: `https://api.velocityai.com.au/webhooks/resend`
4. Select the events to subscribe to:

| Event              | Description                        | Recommended |
|--------------------|------------------------------------|-------------|
| `email.sent`       | Email accepted by Resend           | Yes         |
| `email.delivered`  | Email delivered to recipient        | Yes         |
| `email.opened`     | Recipient opened the email          | Yes         |
| `email.clicked`    | Recipient clicked a link            | Yes         |
| `email.bounced`    | Email bounced                       | Yes         |
| `email.complained` | Recipient marked as spam            | Yes         |

5. Click **Save**.

### 5.3 Verify Webhook Signatures

Always verify the webhook signature to ensure requests are genuinely from Resend:

```javascript
import { Webhook } from 'svix';

const webhook = new Webhook(process.env.RESEND_WEBHOOK_SECRET);

export async function POST(request) {
  const body = await request.text();
  const headers = {
    'svix-id': request.headers.get('svix-id'),
    'svix-timestamp': request.headers.get('svix-timestamp'),
    'svix-signature': request.headers.get('svix-signature'),
  };

  try {
    const event = webhook.verify(body, headers);
    // Process the event
    console.log('Webhook event:', event.type);
    return new Response('OK', { status: 200 });
  } catch (error) {
    console.error('Webhook verification failed:', error);
    return new Response('Invalid signature', { status: 401 });
  }
}
```

### 5.4 Handle Key Events

```javascript
function handleWebhookEvent(event) {
  switch (event.type) {
    case 'email.delivered':
      // Update email status in database
      break;
    case 'email.opened':
      // Track engagement metrics
      break;
    case 'email.bounced':
      // Flag email address, prevent future sends
      break;
    case 'email.complained':
      // Immediately unsubscribe, flag for review
      break;
  }
}
```

---

## 6. Sending Addresses

Configure the following sender identities in Resend:

| Address                          | Use Case                          |
|----------------------------------|-----------------------------------|
| `mitchell@velocityai.com.au`     | Personal emails, follow-ups       |
| `hello@velocityai.com.au`       | General enquiries, welcome emails |
| `bookings@velocityai.com.au`    | Discovery call confirmations      |
| `noreply@velocityai.com.au`     | System notifications              |

---

## 7. Checklist

- [ ] Resend account created
- [ ] velocityai.com.au domain added
- [ ] SPF record configured
- [ ] DKIM records configured (3 CNAME records)
- [ ] DMARC record configured (start with `p=none`)
- [ ] DNS records verified in Resend dashboard
- [ ] API keys created and stored securely
- [ ] Test email sent successfully
- [ ] Webhook endpoint deployed
- [ ] Webhook registered in Resend dashboard
- [ ] Webhook signature verification implemented
- [ ] Sending addresses configured
- [ ] DMARC policy upgraded to `p=quarantine` (after 2–4 weeks)
- [ ] DMARC policy upgraded to `p=reject` (after confirming no issues)

---

## 8. Useful Resources

- [Resend Documentation](https://resend.com/docs)
- [Resend Node.js SDK](https://github.com/resend/resend-node)
- [DNS Checker](https://dnschecker.org)
- [DMARC Analyser](https://www.dmarcanalyzer.com)
- [Mail Tester](https://www.mail-tester.com) — Test email deliverability score
