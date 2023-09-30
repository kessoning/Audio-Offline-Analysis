// Create an instance of the OfflineAnalyzer class
OfflineAnalyzer offlineAnalyzer;

// Initial size of the ellipse
float ellipseSize = 25;

void setup() {
  // Set up the canvas size
  size(400, 400);

  // Initialize the offlineAnalyzer object with file names for volume and beat data
  offlineAnalyzer = new OfflineAnalyzer("data.txt", "beatmap.txt");
}

void draw() {

  // Clear the canvas with a black background
  background(0);
  
  // Use frameCount as the index to analyze data for the current frame
  int index = frameCount;
  
  // Analyze the volume data for the current frame
  offlineAnalyzer.analyzeVolumeFromFile(index);
  
  // Analyze the beat data for the current frame
  offlineAnalyzer.analyzeBeatFromFile(index);
  
  // Get the frame number corresponding to the current volume value
  int volumeFrame = offlineAnalyzer.getCurrentVolumeFrame();
  
  // Get the current volume value
  float volume = offlineAnalyzer.getCurrentVolume();
  
  // Get the frame number corresponding to the current beat value
  int beatFrame = offlineAnalyzer.getCurrentBeatFrame();
  
  // Get the flag indicating whether a beat is present in the current frame
  boolean isBeat = offlineAnalyzer.getIsBeat();
  
  // If there's a beat, increase the size of the ellipse
  if (isBeat) {
    ellipseSize = 125;
  }
  
  // Set the ellipse drawing mode to CENTER
  ellipseMode(CENTER);
  
  // Set the fill color based on the volume value, assuming volume is normalized between 0 and 1
  fill(volume * 255);
  
  // Disable stroke for the ellipse
  noStroke();
  
  // Draw the ellipse at the center of the canvas with the current ellipseSize
  ellipse(width/2, height/2, ellipseSize, ellipseSize);
  
  // If the ellipse size is greater than 25, decrement it to create a shrinking effect
  if (ellipseSize > 25) {
    ellipseSize--;
  }
}
