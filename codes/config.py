CONFIG = {
    "ambp": {
        "name": "Amanda Building Permits",
        "log_dir": "/home/oracle/scripts/Interface/Paymentus/AMBP/log",
        "in_dir": "/home/oracle/scripts/Interface/Paymentus/AMBP/in",
        "archive_dir": "/home/oracle/scripts/Interface/Paymentus/AMBP/archive",
        "received_dir": "/home/oracle/scripts/Interface/Paymentus/AMBP/received",
        "deposit_in": "/opt/fx/PAYMENTUS/INBOUND/RAW/AMBP/DEPOSIT/",
        "deposit_out": "/opt/fx/PAYMENTUS/INBOUND/PROCESSED/AMBP/DEPOSIT/",
        "posting_in": "/opt/fx/PAYMENTUS/INBOUND/RAW/AMBP/POSTING/",
        "posting_out": "/opt/fx/PAYMENTUS/INBOUND/PROCESSED/AMBP/POSTING/",
        "returns_in": "/opt/fx/PAYMENTUS/INBOUND/RAW/AMBP/RETURNS/",
        "returns_out": "/opt/fx/PAYMENTUS/INBOUND/PROCESSED/AMBP/RETURNS/",
        "return_emails": ["building@kitchener.ca", "Scott.Xu@kitchener.ca", "Tatiana.Makarova@kitchener.ca"]
    },
    "amls": {
        "name": "Amanda Legal Services",
        "log_dir": "/home/oracle/scripts/Interface/Paymentus/AMLS/log",
        "in_dir": "/home/oracle/scripts/Interface/Paymentus/AMLS/in",
        "archive_dir": "/home/oracle/scripts/Interface/Paymentus/AMLS/archive",
        "received_dir": "/home/oracle/scripts/Interface/Paymentus/AMLS/received",
        "deposit_in": "/opt/fx/PAYMENTUS/INBOUND/RAW/AMLS/DEPOSIT/",
        "deposit_out": "/opt/fx/PAYMENTUS/INBOUND/PROCESSED/AMLS/DEPOSIT/",
        "posting_in": "/opt/fx/PAYMENTUS/INBOUND/RAW/AMLS/POSTING/",
        "posting_out": "/opt/fx/PAYMENTUS/INBOUND/PROCESSED/AMLS/POSTING/",
        "returns_in": "/opt/fx/PAYMENTUS/INBOUND/RAW/AMLS/RETURNS/",
        "returns_out": "/opt/fx/PAYMENTUS/INBOUND/PROCESSED/AMLS/RETURNS/",
        "return_emails": ["licensing@kitchener.ca", "Scott.Xu@kitchener.ca", "Tatiana.Makarova@kitchener.ca"]
    },
    "ampd": {
        "name": "Amanda Planning Permits",
        "log_dir": "/home/oracle/scripts/Interface/Paymentus/AMPD/log",
        "in_dir": "/home/oracle/scripts/Interface/Paymentus/AMPD/in",
        "archive_dir": "/home/oracle/scripts/Interface/Paymentus/AMPD/archive",
        "received_dir": "/home/oracle/scripts/Interface/Paymentus/AMPD/received",
        "deposit_in": "/opt/fx/PAYMENTUS/INBOUND/RAW/AMPD/DEPOSIT/",
        "deposit_out": "/opt/fx/PAYMENTUS/INBOUND/PROCESSED/AMPD/DEPOSIT/",
        "posting_in": "/opt/fx/PAYMENTUS/INBOUND/RAW/AMPD/POSTING/",
        "posting_out": "/opt/fx/PAYMENTUS/INBOUND/PROCESSED/AMPD/POSTING/",
        "returns_in": "/opt/fx/PAYMENTUS/INBOUND/RAW/AMPD/RETURNS/",
        "returns_out": "/opt/fx/PAYMENTUS/INBOUND/PROCESSED/AMPD/RETURNS/",
        "return_emails": ["Scott.Xu@kitchener.ca"]
    }
}
