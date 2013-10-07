package src.data;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import src.Utils;
import src.data.types.Recipe;

public class RecipeReader {
	
	/**
	 * A regex pattern for ingredient counts, including fractions.
	 */
	private static final Pattern countPat = Pattern.compile("(\\d+)[/(\\d+)]?");
	
	/**
	 * Read a recipe text file into a Recipe.
	 * Assumptions about the format of the recipe files are based on the output of the html parser.
	 * @param file The recipe to read.
	 */
	public static Recipe readRecipe(String file) {
		List<String> lines = Utils.readFile(file);
		
		// Remove directories and extension.
		String name = file.substring(file.lastIndexOf('/') + 1, file.lastIndexOf('.')); 
		
		Map<String, Float> ingredients = new HashMap<String, Float>();
		List<String> ingredientInstructions = new LinkedList<String>();
		
		// Process ingredient list (ie. first line of file).
		String[] ingredientList = lines.get(0).split(","); 
		for (int i = 0; i < ingredientList.length; i++) {
			String ingredientStr = ingredientList[i].trim();
					
			// Get ingredient count.
			float ingredientCount = 1.0f;
			int splitIndex = ingredientStr.indexOf(' ');
			if (splitIndex > 0) {
				String countStr = ingredientStr.substring(0, splitIndex);
				Matcher countMatcher = countPat.matcher(countStr);
				if (countMatcher.matches()) {
					if (countStr.length() > 1 && countStr.charAt(1) == '/') {
						if (countStr.length() > 2)
							ingredientCount = Float.parseFloat(countMatcher.group(1)) / Float.parseFloat(countMatcher.group(2));
						else
							ingredientCount = Float.parseFloat(countStr.substring(0, countStr.length() - 1));
					}
					else 
						ingredientCount = Float.parseFloat(countStr);
					ingredientStr = ingredientStr.substring(splitIndex+1, ingredientStr.length());
				}
			}
			
			// Process ingredient name and instructions if ingredient is complex (instructions are introduced by parentheses).
			String ingredient = ingredientStr;
			splitIndex = ingredientStr.indexOf('(');
			if (splitIndex > 0) {
				ingredient = ingredientStr.substring(0, splitIndex);
				ingredientInstructions.add(ingredientStr.substring(splitIndex + 1, ingredientStr.length()));
			}
			ingredients.put(ingredient, ingredientCount);
		}
		Recipe recipe = new Recipe(name, ingredients, ingredientInstructions.size());
		
		// Process instructions.
		List<String> instructions = new ArrayList<String>(); // this needs to be an array for access by index when building trigrams
		for (String ingredientInstruction: ingredientInstructions)
			instructions.addAll(Utils.tokenize(ingredientInstruction));
		for (int j = 1; j < lines.size(); j++) 
			instructions.addAll(Utils.tokenize(lines.get(j)));
		recipe.setInstructions(instructions);
		return recipe;
	}

}
