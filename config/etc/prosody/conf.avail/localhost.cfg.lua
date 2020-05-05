-- Section for localhost

-- This allows clients to connect to localhost. No harm in it.
VirtualHost "localhost"
    ssl = {
        key = "/etc/prosody/certs/localhost.key";
        certificate = "/etc/prosody/certs/localhost.crt";
    }

