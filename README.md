# twitter-sentiment-analysis
This is our project repository for project II of Computational Intelligence Lab course at ETH Zurich.

## Train the Glove Word Embedding

- cd glove
- ./train.sh args1, args2, args3
	- args1 -> corpus file path
	- args2 -> MAX_ITER
	- args3 -> NUM_THREADS

We can tweak more parameters have a look at train.sh in glove folder

## Twitter LDA

- cd twitter-lda
- ant build
- java -cp bin TwitterLDA/TwitterLDAmain
- Change parameters
	- filelist_test.txt -> All the corpous
	- modelParameters-test.txt -> model params goes here