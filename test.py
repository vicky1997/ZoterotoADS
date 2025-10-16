import zotads

zots = zotads.zot()
adsabs = zotads.adslib()

adstoken='JiVLRHWVuTQ4BrdzhxI0qpGfPp97GHB3UwAaap0f'
zotlibrary_id = '5971476'
zotlibrary_type = 'user'
zotapi_key = 'Jtw0900hfKMTrVvW3g2eZrxp'

adsabs.gettoken(adstoken)
zots.getlib(zotlibrary_id,zotlibrary_type,zotapi_key)

collection_id = '3XNPFZWA'

zots.getcollection(collection_id)
zotads.generatebibtex(zots,adsabs)