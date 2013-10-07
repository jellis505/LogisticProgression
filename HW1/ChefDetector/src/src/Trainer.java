package src;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.util.Arrays;

import cc.mallet.classify.MaxEntTrainer;
import cc.mallet.types.InstanceList;

/**
 * Main class for this project.
 * @author ouyangj
 */

public class Trainer {

	/**
	 * @param args Expected arguments are
	 * 0 - mode ("bagofwords", "backoff", or "trigram")
	 * 1 - directory of saved Instances
	 * 2 - filename where the model is to be saved
	 */
	public static void main(String[] args) throws IOException {
		System.out.println("Training...");
		String mode = args[0];
		String inputDirname = args[1];
		String outputFilename = args[2];
		
		// Read in training Instances.
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
		
		// Train and save model.
		ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream(new File(outputFilename)));
		out.writeObject(new MaxEntTrainer().train(instances)); // this can be any trainer
		out.close();
		System.out.println("...Done.");
	}

}
