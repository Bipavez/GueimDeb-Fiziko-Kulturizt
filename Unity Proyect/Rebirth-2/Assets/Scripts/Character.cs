using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public abstract class Character : MonoBehaviour {

	[SerializeField]
	private float speed;
    [SerializeField]
    protected float speedMod;
	protected Vector2 direction;
    private float recoverySpeed;
	// Use this for initialization
    float getSpeed()
    {
        return speed * speedMod;
    }
	void Start() {
        recoverySpeed = 1.5f;
        speedMod = 1f;
		direction = Vector2.zero;
	}

	// Update is called once per frame
	protected virtual void Update() {
        if (speedMod < 1f)
        {
            speedMod += 3f*Time.unscaledDeltaTime;

        }
        if (speedMod > 1f)
        {
            speedMod = 1f;
        }
		Move();
	}
	public void Move() {
			transform.Translate(direction*getSpeed()*Time.deltaTime);
	}
}
