using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MovingScript : MonoBehaviour {

	[SerializeField]
	private float speed;

	private Vector2 direction;
	// Use this for initialization
	void Start() {
		direction = Vector2.zero;
	}

	// Update is called once per frame
	void Update() {
		GetInput();
		MovePlayer();
	}
  public void MovePlayer() {
			transform.Translate(direction*speed*Time.deltaTime);
	}
	public void GetInput() {
		direction = Vector2.zero;
		if (Input.GetKey(KeyCode.W)) {
			direction += Vector2.up;
		}
		if (Input.GetKey(KeyCode.S)) {
			direction += Vector2.down;
		}
		if (Input.GetKey(KeyCode.D)) {
			direction += Vector2.right;
		}
		if (Input.GetKey(KeyCode.A)) {
			direction += Vector2.left;

		}
	}
}
