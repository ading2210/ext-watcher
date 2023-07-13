from modules import updates, crx

#print(updates.check_update("cjpalhdlnbpafiamejdnhcphjbkeiagm", "1.50.0"))
crx_data = updates.download_crx("cjpalhdlnbpafiamejdnhcphjbkeiagm", "/tmp/extension.crx")
crx.extract_crx(crx_data, "/tmp/crx")
