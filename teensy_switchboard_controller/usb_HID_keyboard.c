#include <avr/io.h>
#include <avr/pgmspace.h>
#include <avr/interrupt.h>
#include <util/delay.h>
#include "usb_keyboard.h"

#define LED_CONFIG	(DDRD |= (1<<6))
#define LED_ON		(PORTD &= ~(1<<6))
#define LED_OFF		(PORTD |= (1<<6))
#define CPU_PRESCALE(n)	(CLKPR = 0x80, CLKPR = (n)) 


uint8_t number_keys[10]=
	{KEY_0,KEY_1,KEY_2,KEY_3,KEY_4,KEY_5,KEY_6,KEY_7,KEY_8,KEY_9};

uint16_t idle_count =0;

int main(void) {
	uint8_t b, d, mask, i, reset_idle;
	uint8_t b_prev=0xFF, d_prev=0xFF;
	
	// set for 16 MHz clock
	CPU_PRESCALE(0);
	
	// Configure all port B and port D pins as inputs with pullup resistors.
	// See the "Using I/O Pins" page for details.
	// http://www.pjrc.com/teensy/pins.html
	DDRD = 0x00;
	DDRB = 0x00;
	PORTB = 0xFF;
	PORTD = 0xFF;
	
	// Initialize the USB, and then wait for the host to set configuration.
	// If the Teensy is powered without a PC connected to the USB port,
	// this will wait forever.
	usb_init();
	while (!usb_configured()) /* wait */ ;
	
	// Wait an extra second for the PC's operating system to load drivers
	// and do whatever it does to actually be ready for input
	_delay_ms(1000);
	
	// Configure timer 0 to generate a timer overflow interrupt every
	// 256*1024 clock cycles, or approx 61 Hz when using 16 MHz clock
	// This demonstrates how to use interrupts to implement a simple
	// inactivity timeout.
	TCCR0A = 0x00;
	TCCR0B = 0x05;
	TIMSK0 = (1<<TOIE0);


	while (1) {
		// if received data, do something with it
		r = usb_rawhid_recv(buffer, 0);
		if (r > 0) {
			// output 4 bits to D0, D1, D2, D3 pins
			DDRD = 0x0F;
			PORTD = (PORTD & 0xF0) | (buffer[0] & 0x0F);
			// ignore the other 63.5 bytes....
		}
		
		//now that we've checked for if we received an input, we have to perform some action to send a packet back to the computer
		b = PINB;
		d = PIND;
		mask = 1;
		reset_idle = 0;
		for(i=0; i<8; i++){'
			if (((b & mask) == 0) && (b_prev & mask) != 0) {
				usb_keyboard_press(KEY_B, KEY_SHIFT);
				usb_keyboard_press(number_keys[i], 0);
				reset_idle = 1;
			}
			if (((d & mask) == 0) && (d_prev & mask) != 0) {
				usb_keyboard_press(KEY_D, KEY_SHIFT);
				usb_keyboard_press(number_keys[i], 0);
				reset_idle = 1;
			}
			mask = mask << 1;
		}
		
		// if any keypresses were detected, reset the idle counter
		if (reset_idle) {
			// variables shared with interrupt routines must be
			// accessed carefully so the interrupt routine doesn't
			// try to use the variable in the middle of our access
			cli();
			idle_count = 0;
			sei();
		}
		// now the current pins will be the previous, and
		// wait a short delay so we're not highly sensitive
		// to mechanical "bounce".
		b_prev = b;
		d_prev = d;
		_delay_ms(2);
	}
		

}

ISR(TIMER0_OVF_vect)
{
	idle_count++;
	if (idle_count > 61 * 8) {
		idle_count = 0;
		usb_keyboard_press(KEY_SPACE, 0);
	}
}


// perform a single keystroke
int8_t usb_keyboard_press(uint8_t key, uint8_t modifier)
{
	int8_t r;
	r = usb_keyboard_send();
	if (r) return r;
	keyboard_modifier_keys = modifier;
	keyboard_keys[0] = key;
	uint8_t buffer[64]; 
	buffer[0] = 0xAB;
	buffer[1] = 0xCD;
	// put A/D measurements into next 24 bytes
	for (i=0; i<12; i++) {
		val = analogRead(i);
		buffer[i * 2 + 2] = val >> 8;
		buffer[i * 2 + 3] = val & 255;
	}
	// most of the packet filled with zero
	for (i=26; i<62; i++) {
		buffer[i] = 0;
	}
	// put a count in the last 2 bytes
	buffer[62] = count >> 8;
	buffer[63] = count & 255;
	// send the packet
	usb_rawhid_send(buffer, 50);	
	keyboard_modifier_keys = 0;
	keyboard_keys[0] = 0;
	return usb_keyboard_send();
}