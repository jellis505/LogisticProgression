package src;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.util.Arrays;
import java.util.List;
import java.util.Map;

import src.classify.ProtoInstance;
import src.data.types.Recipe;
import cc.mallet.types.Alphabet;
import cc.mallet.types.FeatureVector;
import cc.mallet.types.Instance;
import cc.mallet.types.InstanceList;
import cc.mallet.types.LabelAlphabet;

public class InstanceBuilder {
	
	/**
	 * Convert a ProtoInstance to a Mallet Instance.
	 * @param proto The ProtoInstance to be converted.
	 * @param featureAlphabet The feature dictionary.
	 * @return The Instance built from proto and featureAlphabet.
	 */
	private static Instance buildInstance(ProtoInstance proto, Alphabet featureAlphabet, LabelAlphabet labelAlphabet) {
		Map<String, Float> features = proto.getFeatures();
		int numFeatures = features.size();
		int[] indices = new int[numFeatures];
		double[] values = new double[numFeatures];
		int i = 0;
		for (String feature: features.keySet()) {
			indices[i] = featureAlphabet.lookupIndex(feature, false);
			values[i] = (double)features.get(feature);
			i++;
		}
		Recipe recipe = proto.getRecipe();
		return new Instance(new FeatureVector(featureAlphabet, indices, values), labelAlphabet.lookupLabel(recipe.getChef()), recipe.getName(), "emptystring");
	}

	/**
	 * @param args Expected arguments are
	 * 0 - mode ("bagofwords", "rares", or "trigram")
	 * 1 - directory of saved Alphabets and ProtoInstances
	 */
	public static void main(String[] args) throws IOException {
		System.out.println("Building Instances...");
		String mode = args[0];
		String tempDirname = args[1];
		
		// Read in ProtoInstances.
		List<ProtoInstance> trainProtos, testProtos;
		ObjectInputStream in = new ObjectInputStream(new FileInputStream(new File(
				Utils.join(Arrays.asList(new String[] {tempDirname + mode, "trainProto", "ser"}), "."))));
		try {
			trainProtos = (List<ProtoInstance>)in.readObject();
		} catch (ClassNotFoundException e) {
			in.close();
			throw new RuntimeException("Unable to read ProtoInstances.");
		}
		in.close();
		in = new ObjectInputStream(new FileInputStream(new File(
				Utils.join(Arrays.asList(new String[] {tempDirname + mode, "testProto", "ser"}), "."))));
		try {
			testProtos = (List<ProtoInstance>)in.readObject();
		} catch (ClassNotFoundException e) {
			in.close();
			throw new RuntimeException("Unable to read ProtoInstances.");
		}
		in.close();
		
		// Read in Alphabets.
		Alphabet featureAlphabet;
		in = new ObjectInputStream(new FileInputStream(new File(
				Utils.join(Arrays.asList(new String[] {tempDirname + mode, "featureAlpha", "ser"}), "."))));
		try {
			featureAlphabet = (Alphabet)in.readObject();
		} catch (ClassNotFoundException e) {
			in.close();
			throw new RuntimeException("Unable to read feature dictionary.");
		}
		in.close();
		LabelAlphabet labelAlphabet;
		in = new ObjectInputStream(new FileInputStream(new File(
				Utils.join(Arrays.asList(new String[] {tempDirname + mode, "labelAlpha", "ser"}), "."))));
		try {
			labelAlphabet = (LabelAlphabet)in.readObject();
		} catch (ClassNotFoundException e) {
			in.close();
			throw new RuntimeException("Unable to read label dictionary.");
		}
		in.close();
		
		// Build Instances.
		InstanceList trainInstances = new InstanceList(featureAlphabet, labelAlphabet);
		for (ProtoInstance proto: trainProtos)
			trainInstances.add(buildInstance(proto, featureAlphabet, labelAlphabet));
		InstanceList testInstances = new InstanceList(featureAlphabet, labelAlphabet);
		for (ProtoInstance proto: testProtos)
			testInstances.add(buildInstance(proto, featureAlphabet, labelAlphabet));

		// Save Instances.
		ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream(new File(
				Utils.join(Arrays.asList(new String[] {tempDirname + mode, "train", "ser"}), "."))));
		out.writeObject(trainInstances);
		out.close();
		out = new ObjectOutputStream(new FileOutputStream(new File(
				Utils.join(Arrays.asList(new String[] {tempDirname + mode, "test", "ser"}), "."))));
		out.writeObject(testInstances);
		out.close();
		System.out.println("...Done.");
	}

}
