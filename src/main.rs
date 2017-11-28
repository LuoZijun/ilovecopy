
extern crate image;

use std::time;

use image::GenericImage;
use image::Pixel;
use image::ImageBuffer;


// 486 392
const WIDTH: u32  = 293*512 + 486;
const HEIGHT: u32 = 11*512 + 392;
const SIZE: usize = (WIDTH * HEIGHT) as usize;

// JPEG Max size (in pixels): 65,535 x 65,535 (width x height)

fn worker(){
    println!("Sample: {} * {} = {} pixels", WIDTH, HEIGHT, SIZE);

    let now = time::Instant::now();

    for x in 0..294 {
        let mut img = ImageBuffer::new(if x == 293 { 486 } else { 512 }, HEIGHT);
        img.put_pixel(0, 0, image::Rgb([0, 0, 0]));
        for y in 0..12 {
            let fname = format!("data/l5_{}_{}.jpg", y+1, x+1);
            let dim = image::open(&fname).unwrap();
            dim.pixels().for_each(|(w, h, pixel)|{
                let rgb_pixel = pixel.to_rgb();
                img.put_pixel(w, y*512+h, rgb_pixel);
            });
        }
        img.save(format!("result/{}.png", x+1)).unwrap();
    }
    println!("\nvertical merge duration: {:?}", now.elapsed());

    let now2 = time::Instant::now();
    let mut img = ImageBuffer::new(WIDTH, HEIGHT);
    img.put_pixel(0, 0, image::Rgb([0, 0, 0]));
    for y in 0..294 {
        let fname = format!("result/{}.png", y + 1);
        let dim = image::open(&fname).unwrap();
        dim.pixels().for_each(|(w, h, pixel)|{
            let rgb_pixel = pixel.to_rgb();
            img.put_pixel(y*512+w, h, rgb_pixel);
        });
    }
    img.save("output.png").unwrap();
    println!("\nhorizontal merge duration: {:?}", now2.elapsed());

    let now3 = time::Instant::now();
    println!(":: Resize: {} x {}  -->  {} x {} ...", img.width(), img.height(),
        65535, 3012);
    let new_im = image::imageops::resize(&img, 65535, 3012, image::FilterType::Lanczos3);
    new_im.save("output.resize.jpg").unwrap();
    println!("\nresize duration: {:?}", now3.elapsed());

    println!("\n:: DONE total duration: {:?}", now.elapsed());
}

fn main (){
    worker();
}
