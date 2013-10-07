package src;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.PrintWriter;
import java.util.Arrays;
import java.util.List;

import src.classify.ProtoInstance;

import cc.mallet.classify.Classifier;
import cc.mallet.types.Alphabet;
import cc.mallet.types.Instance;
import cc.mallet.types.InstanceList;

public class Tester {

	/**
	 * @param args Expected values are
	 * 0 - mode ("bagofwords", "rares", "trigram")
	 * 1 - directory of saved Instances
	 * 2 - filename where the trained model is saved
	 * 3 - output filename
	 */
	public static void main(String[] args) throws IOException {
		System.out.println("Testing...");
		String mode = args[0];
		String inputDirname = args[1];
		String modelFilename = args[2];
		String outputFilename = args[3];
		
		// Read in testing Instances.
		InstanceList instances;
		ObjectInputStream in = new ObjectInputStream(new FileInputStream(new File(
				Utils.join(Arrays.asList(new String[] {inputDirname + mode, "train", "ser"}), "."))));
		try {
			instances = (InstanceList)in.readObject();
		} catch (ClassNotFoundException e) {
			in.close();
			throw new RuntimeException("Unable to read Instances.");
		}
		in.close();
		
		// Read in trained model.
		Classifier model;
		in = new ObjectInputStream(new FileInputStream(new File(modelFilename)));
		try {
			model = (Classifier)in.readObject();
		} catch (ClassNotFoundException e) {
			in.close();
			throw new RuntimeException("Unable to read model.");
		}
		in.close();
		
		// Test and write output.
		int correctCount = 0;
		PrintWriter writer = new PrintWriter(outputFilename);
		for (Instance instance: instances) {
			Object gold = instance.getTarget();
			Object output = model.classify(instance).getLabeling().getBestLabel();
			String outcome = "-";
			if (gold.equals(output)) {
				outcome = "+";
				correctCount++;
			}
			writer.print(instance.getName());
			writer.print(",");
			writer.print(gold);
			writer.print(",");
			writer.print(output);
			writer.print(",");
			writer.println(outcome);
		}
		writer.close();
		System.out.println("...Done.");
		System.out.println("Accuracy: " + ((correctCount) / (float)instances.size()));
	}

}
