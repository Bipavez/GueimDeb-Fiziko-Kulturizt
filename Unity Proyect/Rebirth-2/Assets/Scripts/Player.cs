using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Player : Character {

    [SerializeField]
    private Animator anim;

    private bool playerWalking;

    private Vector2 lastMoved;

   
	// Use this for initialization
	void Start() {
		direction = Vector2.zero;
        anim = GetComponent<Animator>();
	}

	// Update is called once per frame

	protected override void Update()
	{
		GetInput();
		base.Update();
	}

	public void GetInput()
	{
        playerWalking = false;
		direction = Vector2.zero;
        


		if (Input.GetKey(KeyCode.W))
		{
			direction += Vector2.up;
            playerWalking = true;
            lastMoved = new Vector2(direction.x, direction.y);

        }
        if (Input.GetKey(KeyCode.S))
		{
			direction += Vector2.down;
            playerWalking = true;
            lastMoved = new Vector2(direction.x, direction.y);
        }
		if (Input.GetKey(KeyCode.D))
		{
			direction += Vector2.right;

            playerWalking = true;
            lastMoved = new Vector2(direction.x, direction.y);
        }
        if (Input.GetKey(KeyCode.A))
        {
            direction += Vector2.left;
            playerWalking = true;
            lastMoved = new Vector2(direction.x, direction.y);
        }

        if (Input.GetKeyDown(KeyCode.Space))
        {
            anim.SetTrigger("Attack");
            base.speedMod = 0.0001f;

        }
        



        anim.SetFloat("MoveX", direction.x);
        anim.SetFloat("MoveY", direction.y);
        anim.SetBool("Walking", playerWalking);
        anim.SetFloat("MovedX", lastMoved.x);
        anim.SetFloat("MovedY", lastMoved.y);
    }
}

