package src.data.types;

public class Token {

	private String word;
	private String pos;
	
	public Token(String word, String pos) {
		this.word = word;
		this.pos = pos;
	}

	public String getWord() {
		return word;
	}

	public String getPos() {
		return pos;
	}

}
