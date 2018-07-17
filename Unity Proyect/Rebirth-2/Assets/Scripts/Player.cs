using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Player : Character {

    [SerializeField]
    private Animator anim;

    private bool playerWalking;

    private Vector2 lastMoved;

    private Vector2 new_dir;

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
        
        
        if (Input.GetAxisRaw("Vertical") != 0)
        {
            new_dir = new Vector2(0f, Input.GetAxisRaw("Vertical"));
            direction += new_dir;
        }
        if (Input.GetAxisRaw("Horizontal") != 0)
        {
            new_dir = new Vector2(Input.GetAxisRaw("Horizontal"), 0f);
            direction += new_dir;
        }
        if (direction.magnitude != 0)
        {
            playerWalking = true;
            lastMoved = new Vector2(direction.x, direction.y);

        }
        
        // Cambiar a algun input predefinido
        if (Input.GetKeyDown(KeyCode.Space))
        {
            anim.SetTrigger("Attack");
            base.speedMod = 0.01f;

        }
        



        anim.SetFloat("MoveX", direction.x);
        anim.SetFloat("MoveY", direction.y);
        anim.SetBool("Walking", playerWalking);
        anim.SetFloat("MovedX", lastMoved.x);
        anim.SetFloat("MovedY", lastMoved.y);
    }
}

