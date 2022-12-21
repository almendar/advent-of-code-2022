import scala.math.Ordering.apply
import scala.collection.mutable.TreeMap
import scala.collection.Iterable
extension (a: Int)
  def times(f: => Unit) =
    var k = a
    while (k > 0) do
      f
      k -= 1

val k = (a: Int, b: Int) => a + b

object Node:
  given Ordering[Node] = Ordering.by((it: Node) => it.value)

class Node(val value: Int) extends Iterable[Node]:

  var prev = this
  var next = this
  var originalNext = this

  override def iterator: Iterator[Node] =
    val self = this
    type State0 = (Node, Boolean)
    val init = (self, true)
    Iterator.unfold(init) {
      case (`self`, false) => None
      case (`self`, true)  => Some(self, (self.next, false))
      case (other, _)      => Some(other, (other.next, false))
    }

  def create(value: Int): Node =
    val n = Node(value)
    val curr_next = this.next
    curr_next.prev = n
    this.next = n
    this.originalNext = n
    n.prev = this
    n.next = curr_next
    n.originalNext = curr_next
    n

  def traverse(n: Int): Node =
    var node = this
    n.times { node = node.next }
    return node

  override def toString(): String = value.toString()

  def printChain(): Unit =
    val acc = Vector.newBuilder[Int]
    acc += this.value

    var iter = this.next
    while (iter != this) do
      acc += iter.value
      iter = iter.next
    println(acc.result())

//   originalNext: Node

val n1 = Node(2)

n1.create(22).create(54)

for (i <- n1) do println(i)
// val n2 = n1.traverse(1)
// n2.printChain()

val map = TreeMap.empty[Node, Int]

// trait AocSolution

// class Day15 extends AocSolution:

//   extension (it: Int)
//     def absoluteValue: Int = it.abs
//     def double: Int = it * 2

// val day15 = Day15()

// import day15._

// val p = 22
// p.absoluteValue
