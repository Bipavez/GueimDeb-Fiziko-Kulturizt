using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public abstract class Character : MonoBehaviour {
	[SerializeField]
	private float speed;

	protected Vector2 direction;
	// Use this for initialization
	void Start() {
		direction = Vector2.zero;
	}

	// Update is called once per frame
	void Update() {
		Move();
	}
	public void Move() {
			transform.Translate(direction*speed*Time.deltaTime);
	}
}
