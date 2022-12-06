# Wikidata Extraction

Main pupose is to create a simple extraction of useful methods to extract KG-triplets and graphs from WikiData.

## Extract Methods:
### General methods
- [ ] Get Wikidata
- [ ] Get Wikidata stats
- [ ] Get relations

### Queries
- [x] GET Nodes by name - [Problem: To many IDs are returned]
- [ ] GET Nodes inbetween (multihop)
- [o] GET Subgraph by Names
- [x] GET Subgraph by NodeID
- [x] GET Edges for given NodeID-pair (1-hop)
- [ ] GET Edge Relation info
- [o] GET Edge by name
- [x] GET Edges by NodeIDs
- [ ] Extra Nodes?
- [ ] GET Adj Matrix
- [ ] GET ADJ AllInOne
- [ ] GET Node/Relation by ID
- [x] Predicate by Ent_ID and Property_ID
- [x] Posticate by Ent_ID and Property_ID
### Not applicable:
- Update nodes
- Uploading nodes
- Delete Obj/Relation

## Issues to discuss:
- Choose correct entity when multiple entities are returned
- Maybe introduce threshold for Choosing 'None', if no good matching entinty were found