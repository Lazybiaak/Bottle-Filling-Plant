package edges

import (
	"image"
	"image/color"
	"image/draw"
	"math"
)

const (
	WindowSize      = 7
	Ratio           = 0.80
	SmoothingFactor = 0.94
	ThinningFactor  = 0
)

type Detector struct {
	original                                image.Image
	gray                                    *image.Gray
	graySize, bufSize                       image.Point
	workRect                                image.Rectangle
	buffer, smoothed                        [][]float32
	bli, res                                [][]uint8
	bgColor, fgColor                        color.Color
	doHysteresis                            bool
	outlineSize, windowSize, thinningFactor int
	ratio, smoothingFactor                  float32
}

func (d *Detector) i2d() (slice [][]uint8) {
	slice = make([][]uint8, d.bufSize.X)
	for i := range slice {
		slice[i] = make([]uint8, d.bufSize.Y)
	}
	return
}

func (d *Detector) f2d() (slice [][]float32) {
	slice = make([][]float32, d.bufSize.X)
	for i := range slice {
		slice[i] = make([]float32, d.bufSize.Y)
	}
	return
}

func isCandidateEdge(bli [][]uint8, smoothed [][]float32, col, row int) (result bool) {
	result = false
	if bli[col][row] == 1 && bli[col][row+1] == 0 {
		if smoothed[col][row+1]-smoothed[col][row-1] > 0 {
			result = true
		}
	} else if bli[col][row] == 1 && bli[col+1][row] == 0 {
		if smoothed[col+1][row]-smoothed[col-1][row] > 0 {
			result = true
		}
	} else if bli[col][row] == 1 && bli[col][row-1] == 0 {
		if smoothed[col][row+1]-smoothed[col][row-1] < 0 {
			result = true
		}
	} else if bli[col][row] == 1 && bli[col-1][row] == 0 {
		if smoothed[col+1][row]-smoothed[col-1][row] < 0 {
			result = true
		}
	}
	return
}

func (d *Detector) computeAdaptiveGradient(col, row int) (grad float32) {
	var numOn, numOff int
	var sumOn, sumOff, avgOn, avgOff float32

	halfWin := d.windowSize / 2
	for i := -d.windowSize / 2; i <= halfWin; i++ {
		for j := -d.windowSize / 2; j <= halfWin; j++ {
			if d.bli[col+j][row+i] != 0 {
				sumOn += d.smoothed[col+j][row+i]
				numOn++
			} else {
				sumOff += d.smoothed[col+j][row+i]
				numOff++
			}
		}
	}
	if sumOff > 0 {
		avgOff = sumOff / float32(numOff)
	}
	if sumOn > 0 {
		avgOn = sumOn / float32(numOn)
	}
	return avgOff - avgOn
}

func (d *Detector) locateZeroCrossings() {
	rect := d.workRect

	for row := rect.Min.Y; row < rect.Max.Y; row++ {
		for col := rect.Min.X; col < rect.Max.X; col++ {
			if isCandidateEdge(d.bli, d.smoothed, col, row) {
				grad := d.computeAdaptiveGradient(col, row)
				d.buffer[col][row] = grad
			} else {
				d.buffer[col][row] = 0.0
			}
		}
	}
}

func estimateThresholds(lap [][]float32, rect image.Rectangle) (low, high float32) {
	var k, count int
	var hist [256]int
	var vmax, vmin, scale, x float32

	vmin = float32(math.Abs(float64(lap[rect.Min.X+20][rect.Min.X+20])))
	vmax = vmin
	for row := rect.Min.Y; row < rect.Max.Y; row++ {
		for col := rect.Min.X; col < rect.Max.X; col++ {
			x = lap[col][row]
			if vmin > x {
				vmin = x
			}
			if vmax < x {
				vmax = x
			}
		}
	}

	scale = 256.0 / (vmax - vmin + 1)

	for row := rect.Min.Y; row < rect.Max.Y; row++ {
		for col := rect.Min.X; col < rect.Max.X; col++ {
			x = lap[col][row]
			k = int((x - vmin) * scale)
			hist[k] += 1
		}
	}

	k = 255
	total := ((rect.Max.Y - 1) * (rect.Max.X - 1))
	max := int(Ratio * float32(total))
	count = hist[k]
	for count < max {
		k--
		if k < 0 {
			break
		}
		count += hist[k]
	}

	high = (float32(k) / scale) + vmin
	low = high / 2
	return
}

func (d *Detector) markConnected(col, row, level int, low, high float32) uint8 {
	var notChainEnd uint8
	rect := d.workRect

	if row >= rect.Max.Y || row < rect.Min.Y || col >= rect.Max.X || col < rect.Min.X {
		return 0
	}
	if d.res[col][row] != 0 {
		return 0
	}
	if d.buffer[col][row] == 0.0 {
		return 0
	}

	if d.buffer[col][row] > low {
		d.res[col][row] = 1
	} else {
		d.res[col][row] = 255
	}

	notChainEnd |= d.markConnected(col+1, row, level+1, low, high)
	notChainEnd |= d.markConnected(col-1, row, level+1, low, high)
	notChainEnd |= d.markConnected(col+1, row+1, level+1, low, high)
	notChainEnd |= d.markConnected(col, row+1, level+1, low, high)
	notChainEnd |= d.markConnected(col-1, row+1, level+1, low, high)
	notChainEnd |= d.markConnected(col-1, row-1, level+1, low, high)
	notChainEnd |= d.markConnected(col, row-1, level+1, low, high)
	notChainEnd |= d.markConnected(col+1, row-1, level+1, low, high)

	if notChainEnd != 0 && level > 0 {
		if d.thinningFactor > 0 && (level%d.thinningFactor != 0) {
			d.res[col][row] = 255
		}
	}
	return 1
}

func (d *Detector) thresholdEdges() {
	d.res = d.i2d()
	rect := d.workRect
	low, high := estimateThresholds(d.buffer, rect)

	if d.doHysteresis == false {
		low = high
	}

	for row := rect.Min.Y; row < rect.Max.Y; row++ {
		for col := rect.Min.X; col < rect.Max.X; col++ {
			if d.buffer[col][row] > high {
				d.markConnected(col, row, 0, low, high)
			}
		}
	}

	for row := rect.Min.Y; row < rect.Max.Y; row++ {
		for col := rect.Min.X; col < rect.Max.X; col++ {
			if d.res[col][row] == 255 {
				d.res[col][row] = 0
			}
		}
	}
}

func (d *Detector) applyVerticalISEF(A, B [][]float32) {
	var b1 float32 = (1.0 - d.smoothingFactor) / (1.0 + d.smoothingFactor)
	b2 := d.smoothingFactor * b1
	x := d.buffer
	y := d.smoothed
	rect := d.workRect

	for col := rect.Min.X; col < rect.Max.X; col++ {
		A[col][rect.Min.Y] = b1 * x[col][rect.Min.Y]
		B[col][rect.Max.Y-1] = b2 * x[col][rect.Max.Y-1]
	}

	for row := rect.Min.Y + 1; row < rect.Max.Y; row++ {
		for col := rect.Min.X; col < rect.Max.X; col++ {
			A[col][row] = b1*x[col][row] + SmoothingFactor*A[col][row-1]
		}
	}

	for row := rect.Max.Y - 2; row >= rect.Min.Y; row-- {
		for col := rect.Min.X; col < rect.Max.X; col++ {
			B[col][row] = b2*x[col][row] + SmoothingFactor*B[col][row+1]
		}
	}

	for col := rect.Min.X; col < rect.Max.X-1; col++ {
		y[col][rect.Max.Y-1] = A[col][rect.Max.Y-		1] = A[col][rect.Max.Y-1]
	}

	for row := rect.Min.Y; row < rect.Max.Y-2; row++ {
		for col := rect.Min.X; col < rect.Max.X-1; col++ {
			y[col][row] = A[col][row] + B[col][row+1]
		}
	}
}

func (d *Detector) applyHorizontalISEF(A, B [][]float32) {
	var b1 float32 = (1.0 - d.smoothingFactor) / (1.0 + d.smoothingFactor)
	b2 := d.smoothingFactor * b1
	x := d.smoothed
	y := d.smoothed
	rect := d.workRect

	for row := rect.Min.Y; row < rect.Max.Y; row++ {
		A[rect.Min.X][row] = b1 * x[rect.Min.X][row]
		B[rect.Max.X-1][row] = b2 * x[rect.Max.X-1][row]
	}

	for col := rect.Min.X + 1; col < rect.Max.X; col++ {
		for row := rect.Min.Y; row < rect.Max.Y; row++ {
			A[col][row] = b1*x[col][row] + SmoothingFactor*A[col-1][row]
		}
	}

	for col := rect.Max.X - 2; col >= rect.Min.X; col-- {
		for row := rect.Min.Y; row < rect.Max.Y; row++ {
			B[col][row] = b2*x[col][row] + SmoothingFactor*B[col+1][row]
		}
	}

	for row := rect.Min.Y; row < rect.Max.Y; row++ {
		y[rect.Max.X-1][row] = A[rect.Max.X-1][row]
	}

	for row := rect.Min.Y; row < rect.Max.Y; row++ {
		for col := rect.Min.X; col < rect.Max.X-1; col++ {
			y[col][row] = A[col][row] + B[col+1][row]
		}
	}
}

func (d *Detector) computeISEF() {
	d.smoothed = d.f2d()
	A := d.f2d()
	B := d.f2d()
	d.applyVerticalISEF(A, B)
	d.applyHorizontalISEF(A, B)
}

func NewEdgeDetector(img image.Image) *Detector {
	return &Detector{
		doHysteresis:    true,
		thinningFactor:  ThinningFactor,
		windowSize:      WindowSize,
		ratio:           Ratio,
		smoothingFactor: SmoothingFactor,
		original:        img,
		bgColor:         image.White.C,
		fgColor:         image.Black.C,
	}
}
