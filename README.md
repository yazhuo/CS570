# CS570
Emory CS570 course project

## Dataset
### Directory
Top directory: `/research/yazhuo/ALL_DATA/CDN/`

Split by costomers: `/research/yazhuo/ALL_DATA/CDN/splitCustomer/`

### Trace Illustration
A sample aggregated request:

`1525059390.677 116.242.110.164 189 1066 463 bc1cc513be92f2dc1cbcaa3fbcc08668ca3720726c8922e4c39fd62d4b16f61d dummyStatus dummyHit dummyToEdge 4096 2441 ecomm`

`timestamp client data_center cutomer bucket object dummyStatus dummyHit dummyToEdge object_size request_size traffic_type`

Note: 
- client refers to a user or machine who sends the request
- customer refers to a content provider, such as CNN.

## Tasks
**Yazhuo**
- [ ] Recency feature extraction (I have implemented data structure to get recency faster, other features should be not that hard to extract)
- [ ] CDN Cache Simulator

**Yanan**
- [ ] ?

**Yibo**
- [ ] ?
