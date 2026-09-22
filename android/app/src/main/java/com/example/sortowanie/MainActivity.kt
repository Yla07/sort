package com.example.sortowanie

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.sortowanie.ui.theme.SortowanieTheme

private val Ink = Color(0xFF202322)
private val Muted = Color(0xFF7B817B)
private val Paper = Color(0xFFF3F1EB)
private val Panel = Color(0xFFE4E8DF)
private val Lime = Color(0xFFD8EE6F)
private val Line = Color(0xFFCDD2C9)
private val BarGreen = Color(0xFFB8CC46)
private val BarPale = Color(0xFFE0E5D7)
private val algorithms = listOf("Bubble sort", "Quick sort", "Insertion sort", "Selection sort")

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent { SortowanieTheme { SortScreen() } }
    }
}

@Composable
private fun SortScreen() {
    var data by remember { mutableStateOf(emptyList<Int>()) }
    var minimum by remember { mutableStateOf("0") }
    var maximum by remember { mutableStateOf("100") }
    var size by remember { mutableStateOf("16") }
    var value by remember { mutableStateOf("") }
    var algorithm by remember { mutableStateOf(algorithms.first()) }
    var message by remember { mutableStateOf("Ready when you are.") }
    var isSorted by remember { mutableStateOf(false) }

    Column(
        modifier = Modifier.fillMaxSize().background(Paper).verticalScroll(rememberScrollState()).padding(20.dp),
        verticalArrangement = Arrangement.spacedBy(18.dp)
    ) {
        Row(
            modifier = Modifier.fillMaxWidth().padding(bottom = 16.dp).border(1.dp, Line).padding(bottom = 18.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text("Sort", color = Ink, fontWeight = FontWeight.Bold, fontSize = 18.sp)
            Row(verticalAlignment = Alignment.CenterVertically) {
                Box(Modifier.size(8.dp).clip(CircleShape).background(Color(0xFF72A86E)))
                Spacer(Modifier.width(8.dp))
                Text("LOCAL ENGINE", color = Muted, fontFamily = FontFamily.Monospace, fontSize = 10.sp)
            }
        }
        Text(
            "Generate a dataset, choose a method, and watch your sorting engine take it apart.",
            modifier = Modifier.padding(start = 8.dp, end = 24.dp, bottom = 18.dp),
            color = Color(0xFF676D66), fontSize = 16.sp, lineHeight = 24.sp
        )
        DatasetControls(
            minimum, { minimum = it }, maximum, { maximum = it }, size, { size = it }, value, { value = it },
            onGenerate = {
                val min = minimum.toIntOrNull()
                val max = maximum.toIntOrNull()
                val count = size.toIntOrNull()
                if (min == null || max == null || count == null || max < min || count !in 1..1000) {
                    message = "Check the range and choose 1-1000 values."
                } else {
                    data = List(count) { (min..max).random() }
                    isSorted = false
                    message = "Generated $count random values."
                }
            },
            onAdd = {
                val number = value.toIntOrNull()
                if (number == null) message = "Enter a whole number first."
                else {
                    data = data + number
                    value = ""
                    isSorted = false
                    message = "Added $number to the dataset."
                }
            },
            onClear = { data = emptyList(); isSorted = false; message = "Dataset cleared." }
        )
        DataPanel(
            data, isSorted, algorithm, { algorithm = it }, message,
            onSort = {
                data = when (algorithm) {
                    "Bubble sort" -> bubbleSort(data)
                    "Quick sort" -> quickSort(data)
                    "Insertion sort" -> insertionSort(data)
                    else -> selectionSort(data)
                }
                isSorted = true
                message = "Sorted ${data.size} values with $algorithm."
            }
        )
    }
}

@Composable
private fun DatasetControls(
    minimum: String, onMinimumChange: (String) -> Unit,
    maximum: String, onMaximumChange: (String) -> Unit,
    size: String, onSizeChange: (String) -> Unit,
    value: String, onValueChange: (String) -> Unit,
    onGenerate: () -> Unit, onAdd: () -> Unit, onClear: () -> Unit
) {
    Column(Modifier.fillMaxWidth().background(Panel).padding(22.dp), verticalArrangement = Arrangement.spacedBy(18.dp)) {
        SectionHeading("01", "Build a dataset")
        Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
            NumberField("Minimum", minimum, onMinimumChange, Modifier.weight(1f))
            NumberField("Maximum", maximum, onMaximumChange, Modifier.weight(1f))
        }
        NumberField("How many values", size, onSizeChange, Modifier.fillMaxWidth())
        Button(
            onClick = onGenerate, modifier = Modifier.fillMaxWidth().height(50.dp),
            colors = ButtonDefaults.buttonColors(containerColor = Ink, contentColor = Color.White), shape = RoundedCornerShape(0.dp)
        ) { Text("Generate random values    ↗", fontWeight = FontWeight.Bold) }
        Spacer(Modifier.height(4.dp))
        Box(Modifier.fillMaxWidth().height(1.dp).background(Line))
        SectionHeading("02", "Add a value")
        Row(horizontalArrangement = Arrangement.spacedBy(12.dp), verticalAlignment = Alignment.Bottom) {
            NumberField("Value", value, onValueChange, Modifier.width(105.dp), "e.g. 42")
            Button(
                onClick = onAdd, modifier = Modifier.weight(1f).height(50.dp),
                colors = ButtonDefaults.buttonColors(containerColor = Color.White, contentColor = Ink), shape = RoundedCornerShape(0.dp)
            ) { Text("Add value    +", fontWeight = FontWeight.Bold) }
        }
        TextButton(onClick = onClear, contentPadding = androidx.compose.foundation.layout.PaddingValues(0.dp)) {
            Text("Clear dataset    ⌫", color = Muted, fontFamily = FontFamily.Monospace, fontSize = 11.sp)
        }
    }
}

@Composable
private fun NumberField(label: String, value: String, onValueChange: (String) -> Unit, modifier: Modifier, placeholder: String = "") {
    Column(modifier) {
        Text(label.uppercase(), color = Muted, fontFamily = FontFamily.Monospace, fontSize = 10.sp)
        OutlinedTextField(
            value = value, onValueChange = onValueChange, modifier = Modifier.fillMaxWidth(), singleLine = true,
            placeholder = { Text(placeholder, color = Muted) }, keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
            shape = RoundedCornerShape(0.dp), colors = androidx.compose.material3.OutlinedTextFieldDefaults.colors(
                focusedBorderColor = Ink, unfocusedBorderColor = Color(0xFFAEB5AA),
                focusedContainerColor = Color.Transparent, unfocusedContainerColor = Color.Transparent
            )
        )
    }
}

@Composable
private fun SectionHeading(number: String, title: String) {
    Row(verticalAlignment = Alignment.CenterVertically) {
        Text(number, color = Color(0xFF9AAA35), fontFamily = FontFamily.Monospace, fontSize = 11.sp)
        Spacer(Modifier.width(12.dp))
        Text(title, color = Ink, fontWeight = FontWeight.Bold, fontSize = 20.sp)
    }
}

@Composable
private fun DataPanel(
    data: List<Int>, isSorted: Boolean, algorithm: String, onAlgorithmChange: (String) -> Unit,
    message: String, onSort: () -> Unit
) {
    var menuExpanded by remember { mutableStateOf(false) }
    val min = data.minOrNull() ?: 0
    val max = data.maxOrNull() ?: 1
    val range = (max - min).coerceAtLeast(1)
    Column(Modifier.fillMaxWidth().background(Color.White).padding(22.dp), verticalArrangement = Arrangement.spacedBy(18.dp)) {
        Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.Bottom) {
            Column {
                Text(if (isSorted) "SORTED OUTPUT" else "INPUT ORDER", color = Muted, fontFamily = FontFamily.Monospace, fontSize = 10.sp)
                Text("${data.size} ${if (data.size == 1) "value" else "values"}", color = Ink, fontWeight = FontWeight.Bold, fontSize = 20.sp)
            }
            Text(if (data.isEmpty()) "Waiting for data" else "Range $min - $max", color = Muted, fontFamily = FontFamily.Monospace, fontSize = 10.sp)
        }
        Box(Modifier.fillMaxWidth().height(220.dp).border(1.dp, Line).padding(horizontal = 4.dp, vertical = 20.dp), contentAlignment = Alignment.Center) {
            if (data.isEmpty()) {
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    Text("Generate or add values", color = Muted, fontSize = 15.sp)
                    Text("Your dataset will appear here.", color = Muted, fontFamily = FontFamily.Monospace, fontSize = 10.sp)
                }
            } else {
                Row(Modifier.fillMaxSize(), horizontalArrangement = Arrangement.spacedBy(4.dp), verticalAlignment = Alignment.Bottom) {
                    data.forEachIndexed { index, item ->
                        val fraction = ((item - min).toFloat() / range).coerceIn(0f, 1f)
                        Box(Modifier.weight(1f).fillMaxHeight(fraction * .9f + .1f).background(if (index % 3 == 2) BarPale else BarGreen))
                    }
                }
            }
        }
        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(10.dp)) {
            Text("Sort with", color = Ink, fontFamily = FontFamily.Monospace, fontSize = 10.sp)
            Box(Modifier.weight(1f)) {
                OutlinedButton(onClick = { menuExpanded = true }, modifier = Modifier.fillMaxWidth(), shape = RoundedCornerShape(0.dp)) { Text(algorithm, color = Ink) }
                DropdownMenu(expanded = menuExpanded, onDismissRequest = { menuExpanded = false }) {
                    algorithms.forEach { option -> DropdownMenuItem(text = { Text(option) }, onClick = { onAlgorithmChange(option); menuExpanded = false }) }
                }
            }
            Button(onClick = onSort, colors = ButtonDefaults.buttonColors(containerColor = Lime, contentColor = Ink), shape = RoundedCornerShape(0.dp)) { Text("Run sort  →", fontWeight = FontWeight.Bold) }
        }
        Text(message, color = Muted, fontFamily = FontFamily.Monospace, fontSize = 11.sp)
    }
}

@Preview(showBackground = true)
@Composable
private fun SortPreview() { SortowanieTheme { SortScreen() } }
