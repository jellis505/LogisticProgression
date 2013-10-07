package src;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectOutputStream;
import java.util.Arrays;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;

import src.classify.FeatureExtractor;
import src.classify.ProtoInstance;
import src.data.RecipeReader;
import src.data.types.Recipe;

import cc.mallet.types.Alphabet;
import cc.mallet.types.FeatureVector;
import cc.mallet.types.Instance;
import cc.mallet.types.InstanceList;
import cc.mallet.types.LabelAlphabet;

public class AlphabetBuilder {

	/**
	 * Generate features and build ProtoInstances from recipes.
	 * @param mode "bagofwords", "backoff", or "trigram"
	 * @param filename The list of recipe text files and their labels.
	 * @param inputDirname The directory of recipe text files.
	 * @return
	 */
	private static List<ProtoInstance> buildProtos(String mode, String filename, String inputDirname) {
		List<ProtoInstance> protos = new LinkedList<ProtoInstance>();
		for (String line: Utils.readFile(filename)) {
			String[] parts = line.split(",");
			Recipe recipe = RecipeReader.readRecipe(inputDirname + parts[0] + ".txt");
			recipe.setChef(parts[1]);
			Map<String, Float> features = FeatureExtractor.getAllFeatures(recipe, mode);
			protos.add(new ProtoInstance(recipe, features));
		}
		return protos;
	}
	
	/**
	 * Get a List of features that appear in fewer than 5 recipes
	 * @param protos The ProtoInstances of the recipes.
	 * @return A List of rare features.
	 */
	private static List<String> getRares(List<ProtoInstance> protos) {
		List<String> rareFeatures = new LinkedList<String>();		
		Map<String, Utils.Counter> rareCounts = new HashMap<String, Utils.Counter>();
		for (ProtoInstance proto: protos) 
			for (String feature: proto.getFeatures().keySet()) {
				if (feature.startsWith("bow_")) {
					if (!rareCounts.containsKey(feature)) 
						rareCounts.put(feature, new Utils.Counter());
					rareCounts.get(feature).increment();
				}
			}
		for (String feature: rareCounts.keySet()) 
			if (rareCounts.get(feature).value() < 5) // this number is arbitrary
				rareFeatures.add(feature);
		return rareFeatures;
	}
	
	/**
	 * Modify a List of ProtoInstances in place by replacing rare features with a RAREWORD feature.
	 * @param rareFeatures A List of rare features.
	 * @param protos The ProtoInstances to modify.
	 */
	private static void backoff(List<String> rareFeatures, List<ProtoInstance> protos) {
		for (ProtoInstance proto: protos) {
			Map<String, Float> oldFeatures = proto.getFeatures();
			Map<String, Float> newFeatures = new HashMap<String, Float>();
			float totalRares = 0.0f;
			for (String feature: oldFeatures.keySet()) {
				if (!rareFeatures.contains(feature))
					newFeatures.put(feature, oldFeatures.get(feature));
				else
					totalRares++;
			}
			newFeatures.put("bow_RAREWORD", totalRares);
			proto.setFeatures(newFeatures);		
		}
	}
	
	/**
	 * @param args Expected arguments are
	 * 0 - which feature set to use: "bagofwords", "backoff", "trigram"
	 * 1 - training label file
	 * 2 - testing label file
	 * 3 - directory of recipe text files
	 * 4 - directory for outputting Alphabets and ProtoInstances
	 */
	public static void main(String[] args) throws IOException {
		System.out.println("Building feature and label dictionaries...");
		String mode = args[0];
		String trainFilename = args[1];
		String testFilename = args[2];
		String inputDirname = args[3];	
		
		// Build ProtoInstances.
		List<ProtoInstance> trainProtos = buildProtos(mode, trainFilename, inputDirname);
		List<ProtoInstance> testProtos = buildProtos(mode, testFilename, inputDirname);
		
		// Adjust features for backoff.
		if (mode.equals("backoff")) {
			List<String> rareFeatures = getRares(trainProtos);
			backoff(rareFeatures, trainProtos);
			backoff(rareFeatures, testProtos);
		}
		
		// Build Alphabets (feature/label dictionaries).
		Alphabet featureAlphabet = new Alphabet();
		LabelAlphabet labelAlphabet = new LabelAlphabet();
		for (ProtoInstance proto: trainProtos) {
			for (String feature: proto.getFeatures().keySet())
				featureAlphabet.lookupIndex(feature, true);
			labelAlphabet.lookupIndex(proto.getRecipe().getChef(), true);
		}
		
		// Save Alphabets.
		String outputDirname = args[4];
		ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream(new File(
				Utils.join(Arrays.asList(new String[] {outputDirname + mode, "featureAlpha", "ser"}), "."))));
		out.writeObject(featureAlphabet);
		out.close();
		out = new ObjectOutputStream(new FileOutputStream(new File(
				Utils.join(Arrays.asList(new String[] {outputDirname + mode, "labelAlpha", "ser"}), "."))));
		out.writeObject(labelAlphabet);
		out.close();

		// Save ProtoInstances.
		out = new ObjectOutputStream(new FileOutputStream(new File(
				Utils.join(Arrays.asList(new String[] {outputDirname + mode, "trainProto", "ser"}), "."))));
		out.writeObject(trainProtos);
		out.close();
		out = new ObjectOutputStream(new FileOutputStream(new File(
				Utils.join(Arrays.asList(new String[] {outputDirname + mode, "testProto", "ser"}), "."))));
		out.writeObject(testProtos);
		out.close();		
		System.out.println("...Done.");	
	}

}
