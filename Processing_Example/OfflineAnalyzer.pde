/**
 * The OfflineAnalyzer class is designed to analyze audio data from files,
 * specifically focusing on volume and beat information. It reads two separate
 * files containing volume and beat data, and provides methods to analyze and
 * retrieve volume and beat information for specific frames.
 */
class OfflineAnalyzer {

  // Array to hold volume values read from file
  String[] volumeValues;

  // Array to hold beat values read from file
  String[] beatsValues;

  // Current volume value being analyzed
  float volume;

  // Frame number corresponding to the current volume value
  int volumeFrame;

  // Flag indicating whether a beat is present in the current frame
  boolean isBeat;

  // Frame number corresponding to the current beat value
  int beatFrame;

  /**
   * Constructor initializes the analyzer with file names for volume and beat data.
   * It loads the volume and beat values from the specified files into arrays.
   *
   * @param volumesFileName Name of the file containing volume data
   * @param beatsFileName   Name of the file containing beat data
   */
  OfflineAnalyzer(String volumesFileName, String beatsFileName) {
    // Load volume values from specified file
    volumeValues = loadStrings(volumesFileName);

    // Load beat values from specified file
    beatsValues = loadStrings(beatsFileName);
  }

  /**
   * Analyzes the volume data from file for a specific frame index.
   *
   * @param index The index of the frame to analyze volume for
   */
  void analyzeVolumeFromFile(int index) {
    // Split the line at the specified index by comma to extract the volume data
    String this_value = split(volumeValues[0], ",")[index];

    // Split the extracted volume data by colon to separate the frame number from the volume value
    String[] splitted_values = split(this_value, ":");

    // Extract and store the frame number as an integer
    volumeFrame = Integer.parseInt(splitted_values[0]);

    // Extract the volume value string from the splitted_values array
    String v = splitted_values[1];

    // The volume value string may contain extra characters surrounding the actual value,
    // such as parentheses. This line of code splits the string based on the opening parenthesis "(",
    // and takes the second part (index 1) which should contain the actual volume value and possibly a closing parenthesis.
    v = split(v, "(")[1];

    // Similarly, this line of code splits the string based on the closing parenthesis ")",
    // and takes the first part (index 0) which should now contain just the actual volume value as a string.
    v = split(v, ")")[0];

    // Parse the cleaned-up volume value string to a float and store it in the volume field
    volume = Float.parseFloat(v);
  }

  /**
   * Analyzes the beat data from file for a specific frame index.
   *
   * @param index The index of the frame to analyze beat for
   */
  void analyzeBeatFromFile(int index) {
    // Split the line at the specified index by colon to extract the beat data
    beatFrame = Integer.parseInt(split(beatsValues[index], ":")[0]);

    // Further split the beat data to extract the beat flag
    String b = split(beatsValues[index], ":")[1];
    b = split(b, "(")[1];
    b = split(b, ")")[0];

    // Determine if a beat is present based on the beat flag value
    isBeat = Float.parseFloat(b) > 0;
  }

  /**
   * Retrieves the frame number corresponding to the current volume value.
   *
   * @return The frame number for the current volume value
   */
  int getCurrentVolumeFrame() {
    return volumeFrame;
  }

  /**
   * Retrieves the current volume value.
   *
   * @return The current volume value
   */
  float getCurrentVolume() {
    return volume;
  }

  /**
   * Retrieves the frame number corresponding to the current beat value.
   *
   * @return The frame number for the current beat value
   */
  int getCurrentBeatFrame() {
    return beatFrame;
  }

  /**
   * Retrieves the flag indicating whether a beat is present in the current frame.
   *
   * @return true if a beat is present, false otherwise
   */
  boolean getIsBeat() {
    return isBeat;
  }
}
