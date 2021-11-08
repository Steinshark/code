import java.util.*;
public class Aircraft{
  private String name;
  private int weight;
  private int speed;
  private int seats;
  private int range;

  //aircraft constructor
    public Aircraft(Scanner sc){
    this.name = sc.next();
    this.weight = sc.nextInt();
    this.speed = sc.nextInt();
    this.seats = sc.nextInt();
    this.range = sc.nextInt();
  }

  //prints aircrafts data
  public void showData(){
    System.out.println(name + ": " + weight + " lbs, " + speed + " knots, " +
    seats + " seats, " + range + " nm");
  }

  //checks if aircraft has at least range r
  public boolean inRange(int r){
    return (range >= r);
  }
}
