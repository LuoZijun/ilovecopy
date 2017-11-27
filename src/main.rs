#![allow(dead_code, unused_must_use, non_upper_case_globals, unused_variables, unused_mut, unused_imports)]

extern crate image;

use std::fs::File;
use std::time::{Duration, Instant};
use std::io::Cursor;
use std::io::Write;

// use image::GenericImage;

const BOX_WIDTH: usize  = 512;
const BOX_HEIGHT: usize = 512;

const WIDTH: usize  = BOX_WIDTH * 294;
const HEIGHT: usize = BOX_HEIGHT * 12;
const SIZE: usize   = WIDTH * HEIGHT;


fn read_box(x: u32, y: u32) -> Vec<u8> {
    let dim = image::open("data/l5_2_45.jpg").unwrap();
    dim.raw_pixels()
}

fn put_box(x: u32, y: u32, pixels: &mut [u8]) {
    let _pixels = read_box(x+1, y+1);

    let sx = BOX_WIDTH * x as usize;
    let sy = BOX_HEIGHT * y as usize;

    for col in 0..BOX_WIDTH {
        for row in 0..BOX_HEIGHT {
            let idx = (sx+col) * (sy+row);
            pixels[idx] = _pixels[col*row];
            pixels[idx+1] = _pixels[col*row+1];
            pixels[idx+2] = _pixels[col*row+2];
        }
    }
}

fn main (){
    let now = Instant::now();

    let mut output = Cursor::new(vec![]);
    {
        let mut encoder = image::png::PNGEncoder::new(&mut output);
        let mut pixels: Vec<u8> = vec![0u8; SIZE*3];
        for x in 0..294{
            for y in 0..12 {
                println!("Process  ./data/l5_{:03}_{:03}.jpg  ZONE: SX: {:06} EX: {:06} SY: {:06} EY: {:06}",
                    y, x, x*512, x*512+512, y*512, y*512+512
                 );
                put_box(x as u32, y as u32, &mut pixels);
            }
        }
        encoder.encode(&pixels, WIDTH as u32, HEIGHT as u32, image::ColorType::RGB(1));    
    }
    
    let mut file = File::create("output.jpg").unwrap();
    file.write_all(&output.into_inner());
    let duration = now.elapsed();
    println!("\nDONE: {:?}", duration);
}
