from pymsteams import connectorcard
webhook = connectorcard("https://epitafr.webhook.office.com/webhookb2/fe98d8f4-571d-4986-9ea5-f04e7702ab25@3534b3d7-316c-4bc9-9ede-605c860f49d2/IncomingWebhook/5afac3a2888f4489af0f4c23439eb970/500a5448-3bbc-4150-a404-a45848e7baee/V21bSas1fsUanrFXS_UW9qnQKVV9fqf09ZFFCDm0oQV6M1")
webhook.text("webhook is working fine")
webhook.send()