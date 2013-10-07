package src.classify;

import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import src.Utils;
import src.Utils.Counter;
import src.data.types.Recipe;

/**
 * A class for extracting features from Recipes.
 * @author ouyangj
 *
 */

public class FeatureExtractor {

	/**
	 * Wrapper for generating features.
	 * @param recipe The recipe from which to extract the features.
	 * @param mode Which feature set to use ("bagofwords", "backoff", "trigram")
	 * @return A Map from feature names to values.
	 */
	public static Map<String, Float> getAllFeatures(Recipe recipe, String mode) {
		Map<String, Float> features = new HashMap<String, Float>();
		
		Map<String, Utils.Counter> nameFeatures = getNameFeatures(recipe);
		for (String feature: nameFeatures.keySet())
			features.put(feature, (float)nameFeatures.get(feature).value());
		
		Map<String, Float> ingredientFeatures = getIngredientFeatures(recipe);
		for (String feature: ingredientFeatures.keySet()) 
			features.put(feature, ingredientFeatures.get(feature));
		
		Map<String, Utils.Counter> instructionFeatures = getInstructionFeatures(recipe, mode.equals("trigram"));
		for (String feature: instructionFeatures.keySet()) 
			features.put(feature, (float)instructionFeatures.get(feature).value());
		
		return features;
	}
	
	/**
	 * Bag of Words features based on the recipe name.
	 * @param recipe The Recipe to generate features for.
	 * @return A Map from words to counts.
	 */
	private static Map<String, Utils.Counter> getNameFeatures(Recipe recipe) {
		Map<String, Utils.Counter> features = new HashMap<String, Utils.Counter>();
		String[] nameTokens = recipe.getName().split("-");
		for (int i = 0; i < nameTokens.length; i++) {
			String featureName = "name_" + nameTokens[i];
			if (!features.containsKey(nameTokens[i]))
				features.put(featureName, new Utils.Counter());
			features.get(featureName).increment();
		}
		return features;
	}
	
	/**
	 * Ingredients and the amounts called for.
	 * @param recipe The Recipe to generate features for.
	 * @return A Map from ingredients to amounts.
	 */
	private static Map<String, Float> getIngredientFeatures(Recipe recipe) {
		Map<String, Float> features = recipe.getIngredients();
		features.put("numComplexIngredients", (float)recipe.numComplexIngredients());
		return features;
	}
	
	/**
	 * A wrapper for getTrigrams() and getBagOfWords().
	 * @param recipe The Recipe to generate features for.
	 * @param trigram True if the features should be trigram; false if they should be bag of words or backoff.
	 * @return A Map from feature names to counts.
	 */
	private static Map<String, Utils.Counter> getInstructionFeatures(Recipe recipe, boolean trigram) {
		if (trigram)
			return getTrigrams(recipe.getInstructions());
		else
			return getBagOfWords(recipe.getInstructions());
	}
	
	/**
	 * Extract all trigrams, using the character * as the start words.
	 * @param words The words to get trigrams from.
	 * @return A Map from trigram names to counts.
	 */
	private static Map<String, Utils.Counter> getTrigrams(List<String> words) {
		Map<String, Utils.Counter> features = new HashMap<String, Utils.Counter>();
		int len = words.size();
		
		if (len > 0) {
			features.put(Utils.join(Arrays.asList(new String[] {"*", "*", words.get(0)}), "_"), new Utils.Counter());
			if (len > 1) {
				features.put(Utils.join(Arrays.asList(new String[] {"*", words.get(0), words.get(1)}), "_"), new Utils.Counter());
				if (len > 2) {
					for (int i = 3; i <= words.size(); i++) {
						String trigram = Utils.join(words.subList(i - 3, i), "_");
						if (!features.containsKey(trigram))
							features.put(trigram, new Utils.Counter());
						features.get(trigram).increment();
					}
				}
			}
		}
		return features;
	}
	
	/**
	 * Get bag of words counts.
	 * @param words The words to count.
	 * @return A Map from words to counts.
	 */
	private static Map<String, Utils.Counter> getBagOfWords(List<String> words) {
		Map<String, Utils.Counter> features = new HashMap<String, Utils.Counter>();
		for (String word: words) {
			String featureName = "bow_" + word;
			if (!features.containsKey(word))
				features.put(featureName, new Utils.Counter());
			features.get(featureName).increment();
		}
		return features;
	}
}
