plugin_paths = { "/usr/share/jitsi-meet/prosody-plugins/" }

-- asap_accepted_issuers = { "sosci" }
-- asap_accepted_audiences = { "sosci"}

-- domain mapper options, must at least have domain base set to use the mapper
muc_mapper_domain_base = "sosci.tv";

turncredentials_secret = "R2AxJmdfrPSBdUWP";

turncredentials = {
  { type = "stun", host = "sosci.tv", port = "4446" },
  { type = "turn", host = "sosci.tv", port = "4446", transport = "udp" },
  { type = "turns", host = "sosci.tv", port = "443", transport = "tcp" }
};

cross_domain_bosh = false;
consider_bosh_secure = true;

VirtualHost "sosci.tv"
        -- enabled = false -- Remove this line to enable this host
        authentication = "anonymous"
        -- authentication = "token"
        -- Properties below are modified by jitsi-meet-tokens package config
        -- and authentication above is switched to "token"
        -- app_id="sosci"
        -- app_secret="hoBEE9ywA5&DVj"
        -- allow_empty_token = false;
        -- Assign this host a certificate for TLS, otherwise it would use the one
        -- set in the global section (if any).
        -- Note that old-style SSL on port 5223 only supports one certificate, and will always
        -- use the global one.
        ssl = {
                key = "/etc/prosody/certs/sosci.tv.key";
                certificate = "/etc/prosody/certs/sosci.tv.crt";
        }
        speakerstats_component = "speakerstats.sosci.tv"
        conference_duration_component = "conferenceduration.sosci.tv"
        -- we need bosh
        modules_enabled = {
            "bosh";
            "pubsub";
            "ping"; -- Enable mod_ping
            "speakerstats";
            "turncredentials";
            "conference_duration";
        }
        c2s_require_encryption = false

Component "conference.sosci.tv" "muc"
    storage = "memory"
    modules_enabled = {
        "muc_meeting_id";
        "muc_domain_mapper";
        --"token_verification";
    }
    admins = { "focus@auth.sosci.tv" }
    muc_room_locking = false
    muc_room_default_public_jids = true

-- internal muc component
Component "internal.auth.sosci.tv" "muc"
    storage = "memory"
    modules_enabled = {
      "ping";
    }
    admins = { "focus@auth.sosci.tv", "jvb@auth.sosci.tv" }
    muc_room_locking = false
    muc_room_default_public_jids = true

VirtualHost "auth.sosci.tv"
    ssl = {
        key = "/etc/prosody/certs/auth.sosci.tv.key";
        certificate = "/etc/prosody/certs/auth.sosci.tv.crt";
    }
    authentication = "internal_plain"

Component "focus.sosci.tv"
    component_secret = "2GBbA5qCiY546Kfa"

Component "speakerstats.sosci.tv" "speakerstats_component"
    muc_component = "conference.sosci.tv"

Component "conferenceduration.sosci.tv" "conference_duration_component"
    muc_component = "conference.sosci.tv"