package src;


import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;

/**
 * Class housing miscellaneous utility methods.
 * @author ouyangj
 */
public class Utils {
	
	/**
	 * Read a file into a list of lines, trimming and discarding blanks.
	 * @param filename The file to be read.
	 * @return A List of the lines of the file.
	 */
	public static List<String> readFile(String filename) {
		try {	
			BufferedReader reader = new BufferedReader(new InputStreamReader(new FileInputStream(filename)));
			ArrayList<String> lines = new ArrayList<String>();
			String curr;
			while ((curr = reader.readLine()) != null) 
				if (curr.trim().length() > 0)
					lines.add(curr.trim());	
			reader.close();
			return lines;
		} catch(IOException e) {
			throw new RuntimeException(e.getMessage());
		}
	}
	/**
	 * Read a file into a list of lines, trimming and discarding blanks.
	 * @param file The file to be read.
	 * @return A List of the lines of the file.
	 */
	public static List<String> readFile(File file) {
		try {	
			BufferedReader reader = new BufferedReader(new InputStreamReader(new FileInputStream(file)));
			ArrayList<String> lines = new ArrayList<String>();
			String curr;
			while ((curr = reader.readLine()) != null) 
				if (curr.trim().length() > 0)
					lines.add(curr.trim());	
			reader.close();
			return lines;
		} catch(IOException e) {
			throw new RuntimeException(e.getMessage());
		}
	}

	
	/**
	 * Python's string.join(words)
	 * @param words A List of words to be concatenated.
	 * @return The words concatenated with intervening single spaces.
	 */
	public static String join(List<String> words) {
		return doJoin(words, " ");
	}
	/**
	 * Python's string.join(words, sep)
	 * @param words A List of words to be concatenated.
	 * @param sep The intervening String to use instead of the default single space.
	 * @return The words concatenated with intervening seps.
	 */
	public static String join(List<String> words, String sep) {
		return doJoin(words, sep);
	}
	/**
	 * Helper method for join() wrappers.
	 * @param words A List of words to be concatenated.
	 * @param sep The intervening String to use instead of the default single space.
	 * @return The words concatenated with intervening seps.
	 */
	private static String doJoin(List<String> words, String sep) {
		if (words.size() == 0)
			return null;
		StringBuffer buff = new StringBuffer();
		int size = words.size();
		for (int i = 0; i < size; i++) {
			buff.append(words.get(i));
			buff.append(sep);
		}
		return buff.toString().trim();
	}
	
	public static final char endingPunctuation[] = new char[] {')', ',', ':', '.'};
	/**
	 * Separate punctuation from adjacent words and tokenize by whitespace.
	 * @param s The sentence to be tokenized.
	 * @return A List of substrings.
	 */
	public static List<String> tokenize(String s) {
		List<String> tokens = new LinkedList<String>();
		
		// Tokenize by whitespace.
		String[] rawTokens = s.split("\\s+");
		for (int i = 0; i < rawTokens.length; i++) {
			String rawToken = rawTokens[i];
			
			// Remove open parentheses.
			if (rawToken.charAt(0) == '(') {
				tokens.add(rawToken.substring(0, 1));
				rawToken = rawToken.substring(1);
			}
			
			// Remove trailing punctuation.
			String temp = null;
			int end = rawToken.length() - 1;
			for (int j = 0; j < endingPunctuation.length; j++) {
				if (end > 0 && rawToken.charAt(end) == endingPunctuation[j]) 
					temp = Character.toString(endingPunctuation[j]);
					rawToken = rawToken.substring(0, end);
					break;
			}
			
			// Remove close parentheses.
			end = rawToken.length() - 1;
			if (end > 0 && rawToken.charAt(end) == ')') {
				tokens.add(rawToken.substring(0, end));
				tokens.add(rawToken.substring(end));
			}
			if (temp != null)
				tokens.add(temp);
		}
		return tokens;
	}

	/**
	 * A convenient integer counter for use with Maps.
	 * Modified from code found on StackOverflow.
	 * @author ouyangj
	 */
	public static class Counter {
		private int value = 0;
		public void increment() { ++value; }
		public int value() { return value; }
	}
}
