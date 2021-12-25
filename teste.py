# Download de dependências

import random

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

import glob
import hashlib

import matplotlib.pyplot as plt

# Parâmetros

numero_rodadas = 1000

# 1 - Imprimir relatório
# 2 - Imprimir estatísticas
# 3 - Exibir estudo aleatório
# 0 - Exibir tudo

operacao = 1

# Contadores reais vazios.

presencial_atrelada_relevante = 0
presencial_atrelada_irrelevante = 0

presencial_desatrelada_relevante = 0
presencial_desatrelada_irrelevante = 0

virtual_atrelada_relevante = 0
virtual_atrelada_irrelevante = 0

virtual_desatrelada_relevante = 0
virtual_desatrelada_irrelevante = 0

vetor_estudo_virtual = []
vetor_estudo_presencial = []

# Abrimos as chaves

with open("private_key.pem", "rb") as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None,
        backend=default_backend()
    )

with open("public_key.pem", "rb") as key_file:
    public_key = serialization.load_pem_public_key(
        key_file.read(),
        backend=default_backend()
    )

# Esse é o loop da contagem de resultados real

if operacao == 1 or operacao == 2 or operacao == 0:
    for file in glob.glob("*.encry"):
        with open(file, 'rb') as enc_file:
            desc = enc_file.read()

        original_message = private_key.decrypt(
            desc,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        ascii_message = original_message.decode("ascii")

        if operacao == 1:

            print("--------------------------------------------------" + file + "--------------------------------------------------")
            hashed = hashlib.md5(original_message)
            print("HASH: " + hashed.hexdigest())
            print(ascii_message)

        # Agora, computamos os resultados.
        if 'Visita virtual' in ascii_message:
            if 'Nao foi relevante' in ascii_message:
                if 'Coordenada desatrelada' in ascii_message:
                    virtual_desatrelada_irrelevante = virtual_desatrelada_irrelevante + 1
                else:
                    virtual_atrelada_irrelevante = virtual_atrelada_irrelevante + 1
            else:
                if 'Coordenada desatrelada' in ascii_message:
                    virtual_desatrelada_relevante = virtual_desatrelada_relevante + 1
                else:
                    virtual_atrelada_relevante = virtual_atrelada_relevante + 1

        if 'Visita presencial' in ascii_message:
            if 'Nao foi relevante' in ascii_message:
                if 'Coordenada desatrelada' in ascii_message:
                    presencial_desatrelada_irrelevante = presencial_desatrelada_irrelevante + 1
                else:
                    presencial_atrelada_irrelevante = presencial_atrelada_irrelevante + 1
            else:
                if 'Coordenada desatrelada' in ascii_message:
                    presencial_desatrelada_relevante = presencial_desatrelada_relevante + 1
                else:
                    presencial_atrelada_relevante = presencial_atrelada_relevante + 1

if operacao == 2 or operacao == 0:
    print("-------------------------------------------------------------------------------------------")
    # Computar resultados

    total_atrelada_virtual = virtual_atrelada_irrelevante + virtual_atrelada_relevante
    total_desatrelada_virtual = virtual_desatrelada_irrelevante + virtual_desatrelada_relevante

    relacao_virtual_atrelada = virtual_atrelada_relevante/total_atrelada_virtual
    relacao_virtual_desatrelada = virtual_desatrelada_relevante/total_desatrelada_virtual

    print("Das visitas virtuais atreladas, " + str(virtual_atrelada_relevante) + " foram relevantes.")
    print("Das visitas virtuais atreladas, " + str(virtual_atrelada_irrelevante) + " não foram relevantes.")
    print("Das visitas virtuais desatreladas, " + str(virtual_desatrelada_relevante) + " foram relevantes.")
    print("Das visitas virtuais desatreladas, " + str(virtual_desatrelada_irrelevante) + " não foram relevantes.")
    print("A fração de coordenadas virtuais atreladas relevantes é " + str(relacao_virtual_atrelada))
    print("A fracão de coordenadas virtuais desatreladas relevantes é " + str(relacao_virtual_desatrelada))
    print("-------------------------------------------------------------------------------------------")

    total_atrelada_presencial = presencial_atrelada_irrelevante + presencial_atrelada_relevante
    total_desatrelada_presencial = presencial_desatrelada_irrelevante + presencial_desatrelada_relevante

    relacao_presencial_atrelada = presencial_atrelada_relevante/total_atrelada_presencial
    relacao_presencial_desatrelada = presencial_desatrelada_relevante/total_desatrelada_presencial

    print("Das visitas presenciais atreladas, " + str(presencial_atrelada_relevante) + " foram relevantes.")
    print("Das visitas presenciais atreladas, " + str(presencial_atrelada_irrelevante) + " não foram relevantes.")
    print("Das visitas presenciais desatreladas, " + str(presencial_desatrelada_relevante) + " foram relevantes.")
    print("Das visitas presenciais desatreladas, " + str(presencial_desatrelada_irrelevante) + " não foram relevantes.")
    print("A fração de coordenadas presenciais atreladas relevantes é " + str(relacao_presencial_atrelada))
    print("A fracão de coordenadas presenciais desatreladas relevantes é " + str(relacao_presencial_desatrelada))
    print("-------------------------------------------------------------------------------------------")
    print("A relação entre coordenadas atreladas e desatreladas em visitas virtuais é " + str(relacao_virtual_atrelada/relacao_virtual_desatrelada) +
          " com " + str(total_atrelada_virtual + total_desatrelada_virtual) + " visitas.")
    print("A relação entre coordenadas atreladas e desatreladas em visitas presenciais é " + str(relacao_presencial_atrelada/relacao_presencial_desatrelada) +
          " com " + str(total_atrelada_presencial + total_desatrelada_presencial) + " visitas.")


if operacao == 3:
    contador = 0
    for i in range(numero_rodadas):
        contador = contador + 1
        print(contador)
        presencial_atrelada_relevante = 0
        presencial_atrelada_irrelevante = 0

        presencial_desatrelada_relevante = 0
        presencial_desatrelada_irrelevante = 0

        virtual_atrelada_relevante = 0
        virtual_atrelada_irrelevante = 0

        virtual_desatrelada_relevante = 0
        virtual_desatrelada_irrelevante = 0

        for file in glob.glob("*.encry"):
            with open(file, 'rb') as enc_file:
                desc = enc_file.read()
            original_message = private_key.decrypt(
                desc,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )

            ascii_message = original_message.decode("ascii")
            #print(ascii_message)

            if 'Visita virtual' in ascii_message:
                if 'Nao foi relevante' in ascii_message:
                    if bool(random.getrandbits(1)) == 1:
                        virtual_desatrelada_irrelevante = virtual_desatrelada_irrelevante + 1
                    else:
                        virtual_atrelada_irrelevante = virtual_atrelada_irrelevante + 1
                else:
                    if bool(random.getrandbits(1)) == 1:
                        virtual_desatrelada_relevante = virtual_desatrelada_relevante + 1
                    else:
                        virtual_atrelada_relevante = virtual_atrelada_relevante + 1

            if 'Visita presencial' in ascii_message:
                if 'Nao foi relevante' in ascii_message:
                    if bool(random.getrandbits(1)) == 1:
                        presencial_desatrelada_irrelevante = presencial_desatrelada_irrelevante + 1
                    else:
                        presencial_atrelada_irrelevante = presencial_atrelada_irrelevante + 1
                else:
                    if 'Coordenada desatrelada' in ascii_message:
                        presencial_desatrelada_relevante = presencial_desatrelada_relevante + 1
                    else:
                        presencial_atrelada_relevante = presencial_atrelada_relevante + 1

        total_atrelada_virtual = virtual_atrelada_irrelevante + virtual_atrelada_relevante
        total_desatrelada_virtual = virtual_desatrelada_irrelevante + virtual_desatrelada_relevante

        relacao_virtual_atrelada = virtual_atrelada_relevante / total_atrelada_virtual
        relacao_virtual_desatrelada = virtual_desatrelada_relevante / total_desatrelada_virtual

        total_atrelada_presencial = presencial_atrelada_irrelevante + presencial_atrelada_relevante
        total_desatrelada_presencial = presencial_desatrelada_irrelevante + presencial_desatrelada_relevante

        relacao_presencial_atrelada = presencial_atrelada_relevante / total_atrelada_presencial
        relacao_presencial_desatrelada = presencial_desatrelada_relevante / total_desatrelada_presencial

        vetor_estudo_virtual.append(relacao_virtual_atrelada/relacao_virtual_desatrelada)
        vetor_estudo_presencial.append(relacao_presencial_atrelada / relacao_presencial_desatrelada)

    plt.hist(vetor_estudo_virtual, bins=16, rwidth=0.95)
    plt.show()
    plt.clf()

    plt.hist(vetor_estudo_presencial, bins=16, rwidth=0.95)
    plt.show()

