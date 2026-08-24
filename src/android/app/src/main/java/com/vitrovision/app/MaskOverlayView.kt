package com.vitrovision.app

import android.content.Context
import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Matrix
import android.graphics.Paint
import android.graphics.Path
import android.util.AttributeSet
import android.view.View
import com.vitrovision.app.models.Prediction

class MaskOverlayView @JvmOverloads constructor(
    context: Context,
    attrs: AttributeSet? = null,
    defStyleAttr: Int = 0
) : View(context, attrs, defStyleAttr) {

    private var bitmap: Bitmap? = null
    private var predictions: List<Prediction> = emptyList()

    private val plantPaint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
        style = Paint.Style.FILL
        color = Color.argb(80, 0, 200, 83)
    }

    private val leafPaint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
        style = Paint.Style.FILL
        color = Color.argb(80, 41, 121, 255)
    }

    private val otherPaint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
        style = Paint.Style.FILL
        color = Color.argb(60, 255, 255, 255)
    }

    private val strokePaint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
        style = Paint.Style.STROKE
        color = Color.WHITE
        strokeWidth = 2f
    }

    private val matrix = Matrix()

    fun setData(bitmap: Bitmap, predictions: List<Prediction>) {
        this.bitmap = bitmap
        this.predictions = predictions
        requestLayout()
        invalidate()
    }

    override fun onDraw(canvas: Canvas) {
        super.onDraw(canvas)

        val bmp = bitmap ?: return
        val viewW = width.toFloat()
        val viewH = height.toFloat()
        val bmpW = bmp.width.toFloat()
        val bmpH = bmp.height.toFloat()

        val scale = minOf(viewW / bmpW, viewH / bmpH)
        val dx = (viewW - bmpW * scale) / 2f
        val dy = (viewH - bmpH * scale) / 2f

        matrix.reset()
        matrix.setScale(scale, scale)
        matrix.postTranslate(dx, dy)

        canvas.drawColor(Color.BLACK)
        canvas.drawBitmap(bmp, matrix, null)

        for (pred in predictions) {
            val pts = pred.points ?: continue
            if (pts.size < 3) continue

            val path = Path()
            var first = true
            for (pt in pts) {
                if (pt.size >= 2) {
                    val px = pt[0].toFloat() * scale + dx
                    val py = pt[1].toFloat() * scale + dy
                    if (first) {
                        path.moveTo(px, py)
                        first = false
                    } else {
                        path.lineTo(px, py)
                    }
                }
            }
            path.close()

            val className = pred.class_name ?: ""
            when {
                className.equals("plant", ignoreCase = true) -> canvas.drawPath(path, plantPaint)
                className.equals("leaf", ignoreCase = true) -> canvas.drawPath(path, leafPaint)
                else -> canvas.drawPath(path, otherPaint)
            }
            canvas.drawPath(path, strokePaint)
        }
    }
}
