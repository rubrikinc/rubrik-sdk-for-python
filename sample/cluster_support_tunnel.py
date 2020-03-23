# Enable support tunnel
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

enable_support_tunnel = rubrik.cluster_support_tunnel(True)

# Disable support tunnel
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

disable_support_tunnel = rubrik.cluster_support_tunnel(False)