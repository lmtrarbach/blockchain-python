# blockchain-python
Personal project for study blockchain
```mermaid
graph TD;
  A[Client] -->|request transactions| B(Blockchain Node 1);
  B -->|validate and add to blockchain| C(Blockchain Node 2);
  C -->|broadcast to network| D[Other Nodes];
  D -->|receive and validate transactions| E(Blockchain Node 3);
  E -->|add to blockchain| F(Blockchain Node 4);
  F -->|broadcast to network| G[Other Nodes];
  G -->|receive and validate transactions| B;
```

To-do:

- [] Adjust wallet module to use grpc instead of import the blockchain function
- [] Integrate service discovery with the blockchain grpc
- [] Fix genesis block as it is not creating the Meikle tree until receive another transaction 
- [] Add signature validation before add the blocks
