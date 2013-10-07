package src;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectOutputStream;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import src.data.RecipeReader;
import src.data.types.Recipe;

public class Preprocessor {
	
	/**
	 * A regex pattern for ingredient counts, including fractions.
	 */
	private static final Pattern countPat = Pattern.compile("(\\d+)[/(\\d+)]?");
	
	/**
	 * Read a recipe text file, save a partially-completed Recipe, and output the instructions for POS-tagging.
	 * Assumptions about the format of the recipe files are based on the output of the html parser.
	 * @param file The recipe to read.
	 * @param tempDirname The directory for instructions that need to be POS-tagged.
	 * @param serDirname The directory for saving partially-completed Recipes.
	 */
	private static void processRecipe(File file, String tempDirname, String serDirname) throws IOException {
		List<String> lines = Utils.readFile(file);
		String name = file.getName();
		name = name.substring(0, name.indexOf('.')); // extension removed
		
		PrintWriter writer = new PrintWriter(serDirname + name + ".temp"); // write out instructions for POS-tagging
		
		Map<String, Float> ingredients = new HashMap<String, Float>();
		int complexIngredientCount = 0;
		
		String[] ingredientList = lines.get(0).split(","); // first line of the recipe is the ingredient list
		for (int i = 0; i < ingredientList.length; i++) {
			String ingredientStr = ingredientList[i].trim();
			
			int splitIndex = ingredientStr.indexOf(' ');
			String countStr = ingredientStr.substring(0, splitIndex);
			
			float ingredientCount = 1.0f;
			Matcher countMatcher = countPat.matcher(countStr);
			if (countMatcher.matches()) {
				if (countStr.charAt(1) == '/')
					ingredientCount = Float.parseFloat(countMatcher.group(1)) / Float.parseFloat(countMatcher.group(2));
				else
					ingredientCount = Float.parseFloat(countStr);
				ingredientStr = ingredientStr.substring(splitIndex+1, ingredientStr.length());
			}
			String ingredient = ingredientStr;
			splitIndex = ingredientStr.indexOf('('); // complex ingredient instructions are surrounded by parentheses
			if (splitIndex > 0) {
				ingredient = ingredientStr.substring(0, splitIndex);
				complexIngredientCount++;
				
				String instruction = ingredientStr.substring(splitIndex + 1, ingredientStr.indexOf(')')); // complex ingredient instruction
				writer.print(instruction);
				writer.println("."); 
			}
			ingredients.put(ingredient, ingredientCount);
		}
		ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream(new File(serDirname + name + ".ser")));
		out.writeObject(new Recipe(name, ingredients, complexIngredientCount));
		out.close();
		
		for (int j = 1; j < lines.size(); j++)
			writer.println(lines.get(j));
		writer.close();
	}
	
	/**
	 * @param args Expected arguments are
	 * 0 - directory of recipe text files
	 * 1 - directory for outputting instructions for pos tagging
	 * 2 - directory for serializing incomplete Recipes
	 */
	public static void main(String[] args) throws IOException {
		File[] recipeTexts = (new File(args[0])).listFiles();
		for (int i = 0; i < recipeTexts.length; i++) 
			processRecipe(recipeTexts[i], args[1], args[2]);
	}

}
