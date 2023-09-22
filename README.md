# baofeng_bfc50

test scripts to discover the bfc50 clone process and memory layout

UPDATE: based on comparing byte strings received from the radio I believe
that its operation is similar to several other chinese radios, notibly the
it uses the bytestring b"PROGRAL" (similar to the b"PROGRAM" used by others)
It also includes the bytestring b"P3107" which is found in the Chirp drivers
for the Retevis H777, the HG_UV98 and the radtel_t18, and tdxone_tdq8a.py

## Observations

### Clone Read
1) The OEM software starts the process by sending "FE 03 30 08"
2) The radio responds with "57 03 30 08 1F 03 FF FF FF FF FF FF"
3) The OEM software sends "45 02 50 52 4F 47 52 41 4C"
4) The radio reponds with 71 bytes of data (see below)

### Cloned Data
1) Assumed to be the 71 bytes received after the first transaction
2) A "blank" config with the default settings and no memories returns: `574502501f03ffffffffffffff00010100850100496201007c0100804562500100800008010ec7d2001a28080e002c002cff01ffff403e353254523e3c272653510d0f0b0eff19dd0b23ff87e527182338230003`
3) Update that config, changing the first channel to 446.000 and it returns:
`574502501f03ffffffffffffffff010100850100496201007c0100804562500100800008010ec7d2021a28080e002c002cff01ffff403e353254523e3c272653510d0f0b0eff19dd0b23ff87e527182838230003`

