import numpy as np
import pandas as pd

from sentence_transformers import SentenceTransformer, util


class Semantic:
    
    def __init__(self, model, descriptions=None):
        self.model = model
        self.embeddings = None
        if descriptions:
            self.embeddings = self.embed_descriptions(descriptions)
        
    def embed_descriptions(self, descriptions_list):
        return self.model.encode(descriptions_list, convert_to_tensor=True, show_progress_bar=True)

    def community_detection(self, embeddings, threshold=0.75, min_community_size=10, init_max_size=1000):
        """
        Function for Fast Community Detection
        Finds in the embeddings all communities, i.e. embeddings that are close (closer than threshold).
        Returns only communities that are larger than min_community_size. The communities are returned
        in decreasing order. The first element in each list is the central point in the community.
        """

        # Compute cosine similarity scores
        cos_scores = util.pytorch_cos_sim(embeddings, embeddings)

        # Minimum size for a community
        top_k_values, _ = cos_scores.topk(k=min_community_size, largest=True)
        print(top_k_values.shape)
        # Filter for rows >= min_threshold
        extracted_communities = []
        for i in range(len(top_k_values)):
            if top_k_values[i][-1] >= threshold:
                new_cluster = []
                # Only check top k most similar entries
                top_val_large, top_idx_large = cos_scores[i].topk(k=init_max_size, largest=True)
                top_idx_large = top_idx_large.tolist()
                top_val_large = top_val_large.tolist()

                if top_val_large[-1] < threshold:
                    for idx, val in zip(top_idx_large, top_val_large):
                        if val < threshold:
                            break

                        new_cluster.append(idx)
                else:
                    # Iterate over all entries (slow)
                    for idx, val in enumerate(cos_scores[i].tolist()):
                        if val >= threshold:
                            new_cluster.append(idx)

                extracted_communities.append(new_cluster)

        # Largest cluster first
        extracted_communities = sorted(extracted_communities, key=lambda x: len(x), reverse=True)

        # Step 2) Remove overlapping communities
        unique_communities = []
        extracted_ids = set()

        for community in extracted_communities:
            add_cluster = True
            for idx in community:
                if idx in extracted_ids:
                    add_cluster = False
                    break

            if add_cluster:
                unique_communities.append(community)
                for idx in community:
                    extracted_ids.add(idx)

        return unique_communities


    def find_topk_related(self, embeddings, description, threshold):

        #embed  description
        comp_embedding = self.model.encode(description, convert_to_tensor=True)

        #Compute cosine-similarities
        cosine_scores = util.pytorch_cos_sim(comp_embedding, embeddings)
        #get most similar companies and their indexes in the dataset
        pairs = []
        for i in range(len(cosine_scores[0]-1)):
            pairs.append({'index': [i], 'score': cosine_scores[0][i]})

        return pd.DataFrame(pairs)
#     # Sort scores in decreasing order
#     pairs = sorted(pairs, key=lambda x: x['score'], reverse=True)
#     #delete first element which is the input company itself
#     del pairs[0]
#     #pull most popular companies from dataframe
#     print(pairs)
    