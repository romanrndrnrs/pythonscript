with open("protocol-numbers-1.txt", "r") as f:
    with open("protocol.txt", "w") as p:
        for line in f:
            lineTab = line.split(maxsplit=1)
            typesProto = lineTab[0]

# with open("dhcp_message-type.csv", "r") as f:
#     with open("dhcp_message-type.txt", "w") as p:
#         for line in f:
#             lineTab = line.split(maxsplit=1)
#             typesProto = lineTab[0]