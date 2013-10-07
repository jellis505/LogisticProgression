package src.data.types;

import java.io.Serializable;
import java.util.List;
import java.util.Map;

/**
 * A recipe, consisting of a chef, 
 * a list of (amounts of) ingredients, 
 * the number of complex ingredients (ie. ingredients that require preparation), 
 * and a list of instructions for the dish itself.
 * @author ouyangj
 */

public class Recipe implements Serializable {

	private String name;
	private String chef;
	private Map<String, Float> ingredients;
	private int complexIngredientCount;
	private List<String> instructions;
	
	/**
	 * @param ingredients A Map from ingredient names to amounts.
	 * @param complexIngredientCount The number of complex ingredients (ie. those with instructions for preparing them).
	 */
	public Recipe(String name, Map<String, Float> ingredients, int complexIngredientCount) {
		this.name = name;
		this.ingredients = ingredients;
		this.complexIngredientCount = complexIngredientCount;
	}

	public String getName() {
		return this.name;
	}
	public void setChef(String chef) {
		this.chef = chef;
	}
	public String getChef() {
		return this.chef;
	}
	public Map<String, Float> getIngredients() {
		return this.ingredients;
	}
	public int numComplexIngredients() {
		return this.complexIngredientCount;
	}
	public void setInstructions(List<String> instructions) {
		this.instructions = instructions;
	}
	public List<String> getInstructions() {
		return this.instructions;
	}
}
