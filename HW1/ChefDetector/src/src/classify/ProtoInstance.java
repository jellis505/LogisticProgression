package src.classify;

import java.io.Serializable;
import java.util.Map;

import src.data.types.Recipe;

/**
 * A class representing a recipe and its features.
 * @author ouyangj
 *
 */

public class ProtoInstance implements Serializable {

	private Recipe recipe;
	private Map<String, Float> features;
	
	public ProtoInstance(Recipe recipe, Map<String, Float> features) {
		this.recipe = recipe;
		this.features = features;
	}

	public Recipe getRecipe() {
		return this.recipe;
	}
	public Map<String, Float> getFeatures() {
		return this.features;
	}
	public void setFeatures(Map<String, Float> features) {
		this.features = features;
	}
}
