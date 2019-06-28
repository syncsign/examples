# Draw Full Screen Image Example

This is an example of user application.

## Procedures Explain

- Create a coroutine task
- Waiting for the display node becomes online
- Save a bitmap to the display
- Create a layout and send to the display node, load the bitmap to full screen

## Prepare the Image

- The image must be width: 400px height: 300px; and use Microsoft Paint on Windows to save as "Monochrome Bitmap"
- Or, you can create a "Monochrome Bitmap" with: https://online-converting.com/image/convert2bmp/ :
	+ Choose '1 (mono)';
	+ Upload an image (400px * 300px);
	+ Make sure the converted size is 16.6 KB, download it, overwrite the app/test.bmp

- Kindly note that 'Microsoft Paint' has better conversion quality than online tools.

## Note

- Send image to each display takes 3 minutes.
