# Mixer-Verifier

Team Members: 
Ryan Anderson
Luke Gessler
Sam Prestwood

Our project is to create a tool focusing on verifying a bitcoin mixer’s quality of mixing. We want to explore this from the perspective of a user of a mixer and build a tool for the user. The tool will accept the user’s input and output addresses used with the mixer and determine how anonymous the mixing service is. The tool will use the following criteria in determining risk of deanonymization:

- Presence of direct transaction links between the input and output addresses
- Differences in stated vs. actual delivery times
  (e.g., if a mixing service claims a randomized 24-72hr delay but 5 transactions all take 48 hours, we have reason to suspect the mixing   service is not doing what it claims)
- Size of the anonymity set

