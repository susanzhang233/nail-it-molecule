# -*- coding: utf-8 -*-


from rdkit import Chem
from rdkit.Chem import AllChem



def featurizer( mol, max_length = 10):
    '''
  Parameters
  -------
  mol: rdkit molecule object
  max_length: max_length of molecule to accept

  Returns
  ------
  nodes: an array with atoms encoded by their atomic numbers
  edges: a matrix indicating the bondtype between each of the included atoms
  '''
    nodes = []
    edges = []
  
    #initiate the encoder of bonds
    bond_types = [
          Chem.rdchem.BondType.ZERO,
          Chem.rdchem.BondType.SINGLE,
          Chem.rdchem.BondType.DOUBLE,
          Chem.rdchem.BondType.TRIPLE,
          Chem.rdchem.BondType.AROMATIC,
        ]
    encoder = {j:i for i, j in enumerate(bond_types,1)}
  
  #loop over the atoms within max_length
    for i in range(max_length+1):
    #append each atom's corresponding atomic number to the nodes array
        nodes.append(mol.GetAtomWithIdx(i).GetAtomicNum())
    
        l = []
    #loop over the atoms to generate a matrix
        for j in range(max_length+1):
          #get each of the bonds
            current_bond = mol.GetBondBetweenAtoms(i,j)
            if current_bond == None:#some atoms are not connected
                l.append(0)
            else:
              #if connected, encode that bond
                l.append(encoder.get(current_bond.GetBondType()))

        edges.append(l)#append each list to create a bond interaction matrix
     
    return nodes, edges

def de_featurizer(nodes, edges):
    '''draw out a molecule
    '''
 
    mol = Chem.RWMol()
  
    bond_types = [
          Chem.rdchem.BondType.ZERO,
          Chem.rdchem.BondType.SINGLE,
          Chem.rdchem.BondType.DOUBLE,
          Chem.rdchem.BondType.TRIPLE,
          Chem.rdchem.BondType.AROMATIC,
        ]
    decoder = {i:j for i, j in enumerate(bond_types,1)}

  #create atoms
    for atom in nodes:
        mol.AddAtom( Chem.Atom( int(atom)) )

  #defeaturize bonds with the matrix

    for a in range(len(edges)):
        for b in range(a+1, len(edges)):
            if 0< edges[int(a)][int(b)] <6:
                mol.AddBond(int(a),int(b), decoder.get(edges[int(a)][int(b)]))

    return mol









def make_discriminator(num_atoms):
    '''
    create a discriminator model that takes in two inputs: nodes and edges of a single molecule
  graphic neural network
    '''
  # This is the one!

  #conv_node = layers.Conv2D(
      #32, (3, 3), activation='relu', input_shape=(10, None)
  #)
    conv_edge = layers.Conv1D(32, (3,), activation = 'relu', input_shape = (num_atoms,num_atoms))
    edges_tensor = keras.Input(shape = (num_atoms,num_atoms), name = 'edges')
    x_edge = conv_edge(edges_tensor)
    #x_edge = layers.MaxPooling1D((2,))(x_edge)
    x_edge = layers.Conv1D(64, (3,), activation='relu')(x_edge)
    x_edge = layers.Flatten()(x_edge)
    x_edge = layers.Dense(64, activation = 'relu')(x_edge)

    nodes_tensor = keras.Input(shape = (num_atoms,), name = 'nodes' )
    x_node = layers.Dense(32, activation = 'relu' )(nodes_tensor)
    x_node = layers.Dropout(0.2)(x_node)
    x_node = layers.Dense(64, activation = 'relu')(nodes_tensor)

    main = layers.concatenate([x_node,x_edge], axis = 1)
    main = layers.Dense(32, activation='relu')(main)
    output = layers.Dense(1, activation = 'sigmoid', name = 'label')(main)# number of classes

    return keras.Model(
    inputs = [nodes_tensor, edges_tensor],
    outputs = output
    )



def get_discriminator_loss(real_predictions,fake_predictions):
    real_predictions = tf.sigmoid(real_predictions)#predictions of the real images
    fake_predictions = tf.sigmoid(fake_predictions)#prediction of the images from the generator
    real_loss = tf.losses.binary_crossentropy(tf.ones_like(real_predictions),real_predictions)# as such
    fake_loss = tf.losses.binary_crossentropy(tf.zeros_like(fake_predictions),fake_predictions)
    return real_loss+ fake_loss



def make_generator(num_atoms, noise_input_shape):
    '''create generator model
    '''
    inputs = keras.Input(shape = (noise_input_shape,))
    x = layers.Dense(128, activation="tanh")(inputs)# input_shape = (noise_input_shape,) )#256: filters
    #x = layers.Dropout(0.2)(x)
    x = layers.Dense(256,activation="tanh")(x)
    #x = layers.Dropout(0.2)(x)
    x = layers.Dense(528,activation="tanh")(x)

    #generating edges
    edges_gen = layers.Dense(units =num_atoms*num_atoms)(x)
    edges_gen = layers.Reshape((num_atoms, num_atoms ))(edges_gen)

    nodes_gen = layers.Dense(units = num_atoms)(x)
    #assert nodes_gen.output_shape == (num_atoms)
    #nodes_gen = layers.Reshape(num_atoms, num_atoms)(edges_gen)

  #y = zeros(())
    return keras.Model(
    inputs = inputs,
    outputs = [nodes_gen, edges_gen]
    )

  #return [nodes_gen, edges_gen]


def get_generator_loss(fake_predictions):
    fake_predictions = tf.sigmoid(fake_predictions)#prediction of the images from the generator
    fake_loss = tf.losses.binary_crossentropy(tf.ones_like(fake_predictions),fake_predictions)
    return fake_loss



"""## GAN"""


def train_step(mol,old_gen_loss,old_disc_loss):
    fake_mol_noise = np.random.randn(batch_size, 100)# input for the generator
    with tf.GradientTape() as gen_tape, tf.GradientTape() as disc_tape:

        real_output = discriminator.evaluate(mol[:2])# trainable = False)

        generated_mols = generator(fake_mol_noise)
        fake_output = discriminator(generated_mols)

        gen_loss = get_generator_loss(fake_output)
        disc_loss = get_discriminator_loss(real_output, fake_output)

            #optimizers would improve the performance of the model with these gradients
        gradients_of_gen = gen_tape.gradient(gen_loss, generator.trainable_variables)
        gradients_of_disc= disc_tape.gradient(disc_loss, discriminator.trainable_variables)

        generator_optimizer = tf.optimizers.Adam(1e-4)
        discriminator_optimizer = tf.optimizers.Adam(1e-4)
        generator_optimizer.apply_gradients(zip(gradients_of_gen, generator.trainable_variables))
        discriminator_optimizer.apply_gradients(zip(gradients_of_disc, discriminator.trainable_variables))

        print('generator loss: ', np.mean(gen_loss))
        print('discriminator loss', np.mean(disc_loss))

def train(nodes,edges, epochs):
    for _ in range(epochs):
        gen_loss = 0
        disc_loss = 0
        for n,e in zip(nodes, edges):
            train = [n.reshape(1,11),e.reshape(1,11,11)]
            train_step(train,gen_loss,disc_loss)
      #display.clear_output(wait=True)
    #if (epoch+1)

